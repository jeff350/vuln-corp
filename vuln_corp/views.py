from functools import wraps
from random import *

from flask import render_template, flash, redirect, request, url_for, make_response
from sqlalchemy.exc import *

from vuln_corp import app
from .forms import LoginForm, SignupForm, EditUserForm
from .models import db, User, Session, Groups


def get_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session = None
        user = None
        try:
            session = Session.query.filter(Session.session_id == request.cookies.get('session_id')).first()
            if session is not None:
                user = session.get_user()
        except NoSuchTableError:
            pass
        return f(user=user, session=session, *args, **kwargs)

    return decorated_function


@app.route('/')
@app.route('/index')
def index():
    user = request.cookies.get('session_id')
    return render_template('index.html', title='Home', user=user, group=request.cookies.get('group'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # logs the user out if they are already logged in
    if request.cookies.get('session_id') is not None:
        response = make_response(redirect('/login'))
        response.set_cookie('session_id', '', expires=0)
        response.set_cookie('group', '', expires=0)
        return response

    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(
                'login request Failed for username= "%s", password=%s' % (form.username.data, str(form.password.data)),
                'danger')
            return render_template('login.html', form=form, group=request.cookies.get('group'))
        elif form.validate_on_submit:
            user = User.query.filter(User.username == request.form.get('username')).first()
            password = request.form.get('password')
            if user.exists:
                if user.password == password:
                    session_id = request.cookies.get('session_id', password + str(randint(1, 999)))
                    new_session = Session(user.username, session_id, True)
                    db.session.add(new_session)
                    db.session.commit()
                    response = make_response(redirect('/profile'))
                    response.set_cookie('session_id', value=session_id)
                    group = Groups.query.filter(Groups.id == user.group).first().groupname
                    response.set_cookie('group', value=group)
                    return response
                flash('Password "%s" is incorrect' % form.password.data, 'danger')
            else:
                flash('User "%s" does not exist' % form.username.data, 'danger')
        return render_template('/login', title='Login', group=request.cookies.get('group'))
    elif request.method == 'GET':
        return render_template('login.html', title='Sign in', form=form, group=request.cookies.get('group'))


@app.route("/logout", methods=['GET'])
@get_user
def logout(*args, **kwargs):
    user = kwargs.get('user')
    session = kwargs.get('session')
    session.active = False
    db.session.commit()
    response = make_response(redirect('/index'))
    response.set_cookie('session_id', '', expires=0)
    return response


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    form.group.choices = [(g.id, g.groupname) for g in Groups.query.all()]
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('signup FAILED for requested username="{}", email="{}"'.format(form.username.data,
                                                                                 str(form.email.data)), 'danger')
            return render_template('signup.html', title='Signup', form=form, group=request.cookies.get('group'))
        else:
            newuser = User(request.form.get('username'), request.form.get('firstname'), request.form.get('lastname'),
                           request.form.get('email'), request.form.get('password'), request.form.get('group'))
            db.session.add(newuser)
            db.session.commit()
            flash('Signup successful for requested username="{}", email="{}"'.format(form.username.data,
                                                                                     str(form.email.data)), 'success')
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form, group=request.cookies.get('group'))


@app.route('/profile')
@get_user
def profile(*args, **kwargs):
    user = kwargs.get('user')
    session = kwargs.get('session')
    return render_template('profile.html', user=user, session=session, group=request.cookies.get('group'))


@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


@app.route('/users')
@get_user
def users(*args, **kwargs):
    user = kwargs.get('user')
    session = kwargs.get('session')
    users = User.query.all()
    return render_template('show_users.html', users=users, user=user, group=request.cookies.get('group'))


@app.route('/sessions')
@get_user
def sessions(*args, **kwargs):
    user = kwargs.get('user')
    session = kwargs.get('session')
    sessions = Session.query.all()
    return render_template('show_sessions.html', sessions=sessions, user=user, group=request.cookies.get('group'))


@app.route('/about')
@get_user
def about(*args, **kwargs):
    user = kwargs.get('user')
    session = kwargs.get('session')
    return render_template('about.html', group=request.cookies.get('group'))


@app.route('/users/<username>')
@get_user
def viewuser(username, *args, **kwargs):
    user = kwargs.get('user')
    session = kwargs.get('session')
    viewuser = User.query.filter(User.username == username).first()
    return render_template('user.html', session=session, user=user, viewuser=viewuser,
                           group=request.cookies.get('group'))


@app.route('/settings', methods=['GET', 'POST'])
@get_user
def settings(*args, **kwargs):
    user = kwargs.get('user')
    session = kwargs.get('session')
    form = EditUserForm(request.form)
    form.group.choices = [(g.id, g.groupname) for g in Groups.query.all()]
    # initialize form with current data
    form.firstname.default = user.firstname.title()
    form.lastname.default = user.lastname.title()
    form.email.default = user.email
    form.password.default = user.password
    form.group.default = int(user.group)
    form.process()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Error Validating form', 'danger')
            return render_template('/settings.html', form=form, user=user, session=session,
                                   group=request.cookies.get('group'))
        elif form.validate_on_submit():
            user.firstname = request.form.get('firstname')
            user.lastname = request.form.get('lastname')
            user.password = request.form.get('password')
            user.email = request.form.get('email')
            user.group = request.form.get('group')
            db.session.commit()
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('/settings.html', user=user, session=session, form=form,
                               group=request.cookies.get('group'))


@app.route('/unauthorized')
def unauthorized():
    return render_template('/unauthorized.html', group=request.cookies.get('group'))
