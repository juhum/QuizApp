from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(10000))


class Questions_choices(db.Model):
    choice_id = db.Column(db.Integer, primary_key=True)
    answer1 = db.Column(db.String(300))
    answer2 = db.Column(db.String(300))
    answer3 = db.Column(db.String(300))
    answer4 = db.Column(db.String(300))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    nick_name = db.Column(db.String(150))
    points = db.Column(db.BigInteger)

