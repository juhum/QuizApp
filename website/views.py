from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Questions, Question_choices, User_question_answers

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
                           current_question_index=current_question_index, user=user)


@views.route('/submit_answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    selected_choice = request.form.get('choice')

    # Implement your logic to check the selected choice and update points or store the answer

    # Redirect to the next question or result page
    return redirect(url_for('views.quiz'))