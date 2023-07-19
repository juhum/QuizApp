from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Questions, Question_choices, User_question_answers
from website import db

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = Questions.query.all()
    choices = Question_choices.query.all()
    current_question_index = int(request.args.get('question_index', 0))
    user = current_user  # Assuming you are using Flask-Login's current_user

    if request.method == 'POST':
        question_id = int(request.form.get('question_id'))
        choice_id = int(request.form.get('choice'))
        # Save the user's answer and perform necessary actions

        # Check if there are more questions
        if current_question_index + 1 < len(questions):
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
    selected_choice_id = request.form.get('choice')
    current_question_index = int(request.args.get('question_index', 0))
    if not selected_choice_id:
        flash('Please select a choice before submitting the form.')
        return redirect(url_for('views.quiz', question_index=current_question_index))

    selected_choice_id = int(request.form.get('choice'))
    print(f"Selected choice ID: {selected_choice_id}")

    choice = Question_choices.query.get(selected_choice_id)
    is_right_choice = choice.is_right_choice if choice else False
    print(f"Is right choice: {is_right_choice}")

    # Store the user's answer and whether it is correct
    user_answer = User_question_answers(user_id=current_user.user_id, question_id=question_id,
                                        choice_id=selected_choice_id, is_right_choice=is_right_choice)
    db.session.add(user_answer)
    db.session.commit()

    print('Current points before update:', current_user.points)
    if is_right_choice:
        current_user.points += 1
        print('Current points after update:', current_user.points)
        db.session.commit()

    # Check if there are more questions
    questions = Questions.query.all()
    current_question_index = int(request.args.get('question_index', 0))
    if current_question_index + 1 < len(questions):
        next_question_index = current_question_index + 1
        return redirect(url_for('views.quiz', question_index=next_question_index))
    else:
        # Quiz completed, redirect to the completion page
        return redirect(url_for('views.quiz_completed'))



@views.route('/quiz/completed')
@login_required
def quiz_completed():
    # Retrieve the user's answers
    user_answers = User_question_answers.query.filter_by(user_id=current_user.user_id).all()

    # Calculate the number of correct answers
    correct_answers = sum(answer.is_right_choice for answer in user_answers)

    return render_template('quiz_completed.html', correct_answers=correct_answers, user=current_user)
