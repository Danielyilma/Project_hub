from project_hub import app, db
from project_hub.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for
from project_hub.models.user import User
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
@app.route('/home')
@login_required
def home():
    return f"<h1>hello {current_user.full_name}"


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()

        user.full_name=form.full_name.data,
        user.email=form.email.data,
        user.phone_number=form.phone_number.data,
        user.telegram=form.telegram.data,
        user.linkedin = form.linkedin.data
        user.passwords = form.password.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user and user.validate_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    
    return render_template('login.html', form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))