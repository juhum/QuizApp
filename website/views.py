from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Questions, Question_choices, User_question_answers, Quiz_attempt
from website import db
from random import shuffle

views = Blueprint('views', __name__)


@views.route('/')
# @login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = Questions.query.all()
    shuffle(questions)  # Randomize the order of the questions
    questions = questions[:5]  # Select the first 5 questions for the quiz
    choices = Question_choices.query.all()
    current_question_index = int(request.args.get('question_index', 0))
    user = current_user  # Assuming you are using Flask-Login's current_user

    # current_question_index = int(request.args.get('question_index', 0))
    # if current_question_index >= len(questions):
    #     current_question_index = 0

    # Reset the points for the current quiz
    if current_question_index == 0:
        Quiz_attempt.query.filter_by(user_id=current_user.user_id).delete()
        db.session.commit()




    if request.method == 'POST':
        question_id = int(request.form.get('question_id'))
        choice_id = int(request.form.get('choice'))
        # Save the user's answer and perform necessary actions

        # Check if there are more questions
        if current_question_index + 1 < 5:
            next_question_index = current_question_index + 1
            return redirect(url_for('views.quiz', question_index=next_question_index))
        else:
            # Quiz completed, redirect to a result page or any other page
            return redirect(url_for('views.quiz_completed'))

    current_question = questions[current_question_index]
    choices_for_current_question = [choice for choice in choices if choice.question_id == current_question.question_id]

    return render_template("quiz.html", question=current_question, choices=choices_for_current_question,
                           current_question_index=current_question_index, user=user, question_id=current_question.question_id)


@views.route('/submit_answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    questions = Questions.query.all()
    selected_choice_id = request.form.get('choice')
    current_question_index = int(request.args.get('question_index', 0))
    current_question = questions[current_question_index]
    choices = Question_choices.query.all()
    choices_for_current_question = [choice for choice in choices if choice.question_id == current_question.question_id]
    if not selected_choice_id:
        flash('Please select a choice before submitting the form.')
        return render_template("quiz.html", question=current_question, choices=choices_for_current_question,
                               current_question_index=current_question_index, user=current_user,
                               question_id=current_question.question_id)

    selected_choice_id = int(request.form.get('choice'))
    print(f"Selected choice ID: {selected_choice_id}")

    choice = Question_choices.query.get(selected_choice_id)
    is_right_choice = choice.is_right_choice if choice else False
    print(f"Is right choice: {is_right_choice}")

    # Store the user's answer and whether it is correct
    user_answer = User_question_answers(user_id=current_user.user_id, question_id=question_id,
                                        choice_id=selected_choice_id, is_right_choice=is_right_choice)
    db.session.add(user_answer)
    quiz_attempt = Quiz_attempt(user_id=current_user.user_id, question_id=question_id,
                                choice_id=selected_choice_id, is_right_choice=is_right_choice)
    db.session.add(quiz_attempt)

    db.session.commit()



    print('Current points before update:', current_user.points)
    if is_right_choice:
        current_user.points += 1
        quiz_attempt.points += 1
        print('Current points after update:', current_user.points)
        db.session.commit()

    # Check if there are more questions
    current_question_index = int(request.args.get('question_index', 0))
    if current_question_index + 1 < 5:
        next_question_index = current_question_index + 1
        return redirect(url_for('views.quiz', question_index=next_question_index))
    else:
        # Quiz completed, redirect to a result page or any other page
        return redirect(url_for('views.quiz_completed'))


@views.route('/quiz/completed')
@login_required
def quiz_completed():
    # Retrieve the user's answers
    user_answers = User_question_answers.query.filter_by(user_id=current_user.user_id).all()

    # Calculate the number of correct answers
    total_points = sum(answer.is_right_choice for answer in user_answers)

    # Retrieve the points for the current quiz
    quiz_attempts = Quiz_attempt.query.filter_by(user_id=current_user.user_id).all()
    current_quiz_points = sum(attempt.points for attempt in quiz_attempts)

    return render_template('quiz_completed.html', total_points=total_points,
                           current_quiz_points=current_quiz_points, user=current_user)


@views.route('/profile/<username>')
@login_required
def profile(username):
    if not username:
        return "Invalid username", 400

    user = User.query.filter_by(nick_name=username).first()
    if user:
        # Assuming you have a relationship between User and User_question_answers
        user_answers = User_question_answers.query.filter_by(user_id=user.user_id).all()
        total_points = sum(answer.is_right_choice for answer in user_answers)
        return render_template("profile.html", user=current_user, total_points=total_points, name=user.nick_name)
    else:
        # If the user doesn't exist, you can handle the error, redirect, or show a custom message.
        return "User not found", 404



@views.route('/leaderboard')
@login_required
def leaderboard():
    users = User.query.all()

    for user in users:
        user_answers = User_question_answers.query.filter_by(user_id=user.user_id).all()
        user.points = sum(answer.is_right_choice for answer in user_answers)

    # Sort the users by points
    users.sort(key=lambda user: user.points, reverse=True)

    return render_template('leaderboard.html', users=users, user=current_user)


@views.route('/quiz/start')
@login_required
def start_quiz():
    return render_template('quiz_start.html', user=current_user)