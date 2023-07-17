from website import create_app
from website.models import User, Questions, Question_choices, User_question_answers
from website import db

app = create_app()

with app.app_context():
    # question = "What is the capital of France?"
    # is_active = True
    #
    # new_question = Questions(question=question, is_active=is_active)
    # db.session.add(new_question)
    # db.session.commit()
    #
    #     # Rest of the code for adding choices and answers...
    #
    #
    #
    # question_id = 1  # Assuming the ID of the question you want to add choices to is 1
    #
    # choice1 = "Paris"
    # is_right_choice1 = True
    # choice2 = "London"
    # is_right_choice2 = False
    #
    # new_choice1 = Question_choices(question_id=question_id, choice=choice1, is_right_choice=is_right_choice1)
    # new_choice2 = Question_choices(question_id=question_id, choice=choice2, is_right_choice=is_right_choice2)
    #
    # db.session.add(new_choice1)
    # db.session.add(new_choice2)
    # db.session.commit()
    #
    # user_id = 1  # Assuming the ID of the user who answered the question is 1
    # question_id = 1  # Assuming the ID of the question answered is 1
    # choice_id = 1  # Assuming the ID of the choice selected by the user is 1
    # is_right_choice = True  # Assuming the user selected the correct choice
    #
    # new_answer = User_question_answers(user_id=user_id, question_id=question_id, choice_id=choice_id,
    #                                    is_right_choice=is_right_choice)
    #
    # db.session.add(new_answer)
    # db.session.commit()
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
            choice1 = f"Choice 1 for Question {i}"
            is_right_choice1 = True
            choice2 = f"Choice 2 for Question {i}"
            is_right_choice2 = False

            new_choice1 = Question_choices(question_id=question_id, choice=choice1, is_right_choice=is_right_choice1)
            new_choice2 = Question_choices(question_id=question_id, choice=choice2, is_right_choice=is_right_choice2)

            db.session.add(new_choice1)
            db.session.add(new_choice2)
            db.session.commit()

            # Add the answer for the question
            user_id = 1  # Assuming the ID of the user who answered the question is 1
            choice_id = new_choice1.choice_id  # Assuming the correct choice is choice 1

            new_answer = User_question_answers(user_id=user_id, question_id=question_id, choice_id=choice_id,
                                               is_right_choice=True)

            db.session.add(new_answer)
            db.session.commit()

