from website import create_app
from website.models import User, Questions, Question_choices, User_question_answers
from website import db

app = create_app()

with app.app_context():
    for i in range(1, 11):
        question = f"Question {i}"
        is_active = True

        new_question = Questions(question=question, is_active=is_active)
        db.session.add(new_question)
        db.session.commit()

        question_id = new_question.question_id

        # Add choices for the question
        choices_data = [
            {"choice": f"Choice 1 for Question {i}", "is_right_choice": True},
            {"choice": f"Choice 2 for Question {i}", "is_right_choice": False},
            {"choice": f"Choice 3 for Question {i}", "is_right_choice": False},
            {"choice": f"Choice 4 for Question {i}", "is_right_choice": False},
        ]

        correct_choice_id = None

        for choice_data in choices_data:
            new_choice = Question_choices(question_id=question_id, choice=choice_data["choice"],
                                          is_right_choice=choice_data["is_right_choice"])
            db.session.add(new_choice)
            db.session.commit()

            if choice_data["is_right_choice"]:
                correct_choice_id = new_choice.choice_id

        # Add the answer for the question
        user_id = 1  # Assuming the ID of the user who answered the question is 1

        new_answer = User_question_answers(user_id=user_id, question_id=question_id, choice_id=correct_choice_id,
                                           is_right_choice=True)

        db.session.add(new_answer)
        db.session.commit()
