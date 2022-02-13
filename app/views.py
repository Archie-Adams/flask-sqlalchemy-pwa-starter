from flask.wrappers import Response
from app import app
from flask import render_template, flash, request, Flask, redirect
from flask_restful import Resource, Api
from .forms import LogInForm, SignUpForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import logging
from flask import (
    Blueprint, make_response, send_from_directory
)

from app import db, models
from app.models import User

# User Authentication -------------------------------------------------------- #
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    app.logger.info('New user loaded: "%s"', user_id)
    return models.User.query.get(int(user_id))
# ---------------------------------------------------------------------------- #

# Logging -------------------------------------------------------------------- #
from flask.logging import default_handler
app.logger.removeHandler(default_handler)
logging.basicConfig(filename='logs.log', filemode='a', level=logging.DEBUG)
# ---------------------------------------------------------------------------- #

# Routes to enable PWA ------------------------------------------------------- #
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response
# ---------------------------------------------------------------------------- #

# Login/Sign-Up/Logout Routes ------------------------------------------------ #
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).all()
        if user != []:
            login_user(user[0])
            return redirect("home", code=307)
    return render_template(
        'login-signup.html',
        title = 'WEBSITE NAME - Log-In',
        form=form,
        login=True
    )

@app.route('/sign-up', methods=['POST', 'GET'])
def signup():
    form = SignUpForm(request.form)
    if form.validate():
        if models.User.query.filter_by(username=form.username.data).all() != []:
            return "Account name taken."
        db.session.add(models.User(username=form.username.data,
                                   password=form.password.data))
        db.session.commit()
        app.logger.info('New user created: "%s"', form.username.data)
        login_user(User.query.filter_by(username=form.username.data).first())
        return redirect("home", code=307)

    return render_template(
        'login-signup.html',
        title = 'WEBSITE NAME - Sign-Up',
        login=False, # Sets sign up mode for the template.
        form=form
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

# ---------------------------------------------------------------------------- #

# Page routes ---------------------------------------------------------------- #
@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    return render_template(
        'home.html',
        title = 'Home Page Title'
    )

@app.route('/all_tags', methods=['POST', 'GET'])
@login_required
def all_tags():
    return render_template(
        'home.html',
        title = 'All HTML Tags'
    )
# ---------------------------------------------------------------------------- #

# AJAX Response Examples ----------------------------------------------------- #
@app.route('/respond_example_ajax', methods=['POST', 'GET'])
@login_required
def respond_example_ajax():
    data = json.loads(request.data)
    example_request_data = data.get('json_key')

    app.logger.info('User %s clicking button', current_user.id)

    return json.dumps({
        'status': 'OK',
        'response': "Example AJAX response, include any data in JSON format."
    })

@app.route('/respond_list_users', methods=['POST'])
@login_required
def respond_list_users():
    data = json.loads(request.data)
    example_request_data = data.get('json_key')

    app.logger.info('User %s doing a thing.', current_user.id)

    ret = {
        "status": "OK",
        "response": "Database queried successfully.",
        "data":[]
    }
    users = models.User.query.all()
    for user in users:
        ret['data'].append({"id":user.id, "username":user.username})

    return json.dumps(ret)

# ---------------------------------------------------------------------------- #
