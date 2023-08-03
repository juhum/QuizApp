from website import create_app
from website.models import User_question_answers, Question_choices, Questions
from website import db


def delete_previous_questions():
    with app.app_context():
        # Delete User_question_answers first to avoid foreign key constraints
        User_question_answers.query.delete()
        db.session.commit()

        # Delete Question_choices
        Question_choices.query.delete()
        db.session.commit()

        # Delete Questions
        Questions.query.delete()
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        delete_previous_questions()
