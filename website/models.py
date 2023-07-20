from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    nick_name = db.Column(db.String(150))
    points = db.Column(db.Integer, default=0)

    def get_id(self):
        return int(self.user_id)


class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(10000))
    is_active = db.Column(db.Boolean, default=True)


class Question_choices(db.Model):
    choice_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    is_right_choice = db.Column(db.Boolean)
    choice = db.Column(db.String(300))


class User_question_answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))  # Use lowercase 'u'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    choice_id = db.Column(db.Integer, db.ForeignKey('question_choices.choice_id'))
    is_right_choice = db.Column(db.Boolean)

class Quiz_attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))  # Use lowercase 'u'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    choice_id = db.Column(db.Integer, db.ForeignKey('question_choices.choice_id'))
    is_right_choice = db.Column(db.Boolean)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    points = db.Column(db.Integer, default=0)

