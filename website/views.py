from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .models import User, Questions, Question_choices, User_question_answers, Quiz_attempt
from website import db
from random import shuffle

views = Blueprint('views', __name__)


@views.route('/')
# @login_required
def home():
    flash_message = session.get('_flashes')
    session.clear()
    if flash_message:
        session['_flashes'] = flash_message

    return render_template("home.html", user=current_user)


@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if 'quiz_started' not in session:
        return redirect(url_for('views.start_quiz'))
    if 'questions' not in session:
        questions = Questions.query.all()
        shuffle(questions)
        session['questions'] = [question.question_id for question in questions[:5]]

    # Retrieve the randomized list of questions from the session variable
    question_ids = session['questions']
    choices = Question_choices.query.all()
    current_question_index = int(request.args.get('question_index', 0))
    user = current_user  # Assuming you are using Flask-Login's current_user

    question_ids = session['questions']
    questions = Questions.query.filter(Questions.question_id.in_(question_ids)).all()

    # Check if current_question_index is within expected range
    num_answered_questions = Quiz_attempt.query.filter_by(user_id=current_user.user_id).count()
    if current_question_index > num_answered_questions:
        flash('You cannot skip ahead!', category='error')
        return redirect(url_for('views.quiz', question_index=num_answered_questions))
    elif current_question_index < num_answered_questions:
        flash('You cannot go back to previous questions!', category='error')
        return redirect(url_for('views.quiz', question_index=num_answered_questions))
    elif current_question_index == 0 and num_answered_questions > 0:
        flash('You cannot restart the quiz!', category='error')
        return redirect(url_for('views.quiz', question_index=num_answered_questions))

    if request.method == 'POST':

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
                           current_question_index=current_question_index, user=user,
                           question_id=current_question.question_id)



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

    # print(f"Selected choice ID: {selected_choice_id}")
    choice = Question_choices.query.get(selected_choice_id)
    is_right_choice = choice.is_right_choice if choice else False
    # print(f"Is right choice: {is_right_choice}")

    # Store the user's answer and whether it is correct
    user_answer = User_question_answers(user_id=current_user.user_id, question_id=question_id,
                                        choice_id=selected_choice_id, is_right_choice=is_right_choice)
    db.session.add(user_answer)
    quiz_attempt = Quiz_attempt(user_id=current_user.user_id, question_id=question_id,
                                choice_id=selected_choice_id, is_right_choice=is_right_choice)
    db.session.add(quiz_attempt)

    db.session.commit()

    if is_right_choice:
        current_user.points += 1
        quiz_attempt.points += 1
        db.session.commit()

    current_question_index = int(request.args.get('question_index', 0))
    if current_question_index + 1 < 5:
        next_question_index = current_question_index + 1
        return redirect(url_for('views.quiz', question_index=next_question_index))
    else:
        return redirect(url_for('views.quiz_completed'))


@views.route('/quiz/completed')
@login_required
def quiz_completed():
    user_answers = User_question_answers.query.filter_by(user_id=current_user.user_id).all()
    total_points = sum(answer.is_right_choice for answer in user_answers)

    quiz_attempts = Quiz_attempt.query.filter_by(user_id=current_user.user_id).all()
    current_quiz_points = sum(attempt.points for attempt in quiz_attempts)
    session.clear()

    return render_template('quiz_completed.html', total_points=total_points,
                           current_quiz_points=current_quiz_points, user=current_user)


@views.route('/user/<username>')
@login_required
def profile(username):
    session.clear()
    if not username:
        return "Invalid username", 400

    user = User.query.filter_by(nick_name=username).first()
    if user:
        user_answers = User_question_answers.query.filter_by(user_id=user.user_id).all()
        total_points = sum(answer.is_right_choice for answer in user_answers)
        return render_template("profile.html", user=current_user, total_points=total_points, name=user.nick_name)
    else:
        return render_template("user_not_found.html", user=current_user)


@views.route('/leaderboard')
@login_required
def leaderboard():
    session.clear()
    users = User.query.all()

    for user in users:
        user_answers = User_question_answers.query.filter_by(user_id=user.user_id).all()
        user.points = sum(answer.is_right_choice for answer in user_answers)

    # Sort the users by points
    users.sort(key=lambda user: user.points, reverse=True)

    return render_template('leaderboard.html', users=users, user=current_user)


@views.route('/quiz/start', methods=['GET', 'POST'])
@login_required
def start_quiz():
    session.clear()
    session['quiz_started'] = True
    Quiz_attempt.query.filter_by(user_id=current_user.user_id).delete()
    db.session.commit()
    return render_template('quiz_start.html', user=current_user)
