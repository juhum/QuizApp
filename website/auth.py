from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)


@auth.route('/logout')
def logout():
    return "<p>logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nick_name = request.form.get('nickName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 3:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(nick_name) < 2:
            flash("Nickname must be greater than 1 character.", category='error')
        elif password1 != password2:
            flash("Passwords must be the same.", category='error')
        elif len(password1) < 6:
            flash("Password must be greater than 5 characters.", category='error')
        else:
            # add user to database
            pass

    return render_template("sign_up.html")
