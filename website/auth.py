from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # Verify the password using the same hashing algorithm
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password or email. Please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", boolean=True)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nick_name = request.form.get('nickName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 3:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(nick_name) < 2:
            flash("Nickname must be greater than 1 character.", category='error')
        elif password1 != password2:
            flash("Passwords must be the same.", category='error')
        elif len(password1) < 6:
            flash("Password must be greater than 5 characters.", category='error')
        else:
            # Create a new user with hashed password
            new_user = User(email=email, nick_name=nick_name,
                            password=generate_password_hash(password1, method='sha256'), points=0)
            # Save the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
