from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.utilities.login_form import LoginForm
from flask_login import current_user, login_user, logout_user
from app.accounts.models.user import User
from app.utilities.reg_form import RegForm
from werkzeug.urls import url_parse


@app.route('/index')
def index():
    return redirect(url_for('irsystem.home'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash("Welcome Back! {}!".format(current_user.username))
        return redirect(url_for('irsystem.search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash("You have logged in! {}".format(user.username))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login_form.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for your register! {}!'.format(user.username))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template("404.html"), 404

# Database error handling
@app.errorhandler(500)
def database_error(error):
    return render_template("500.html"), 500

@app.shell_context_processor
def make_shell_context():
  return {'db':db, 'User':User}