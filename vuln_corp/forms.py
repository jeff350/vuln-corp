from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, validators, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea

from vuln_corp.choices import ISSUE_STATUS, ISSUE_ASSIGNEES
from .models import User


class LoginForm(Form):
    username = StringField("username", [validators.DataRequired("Please enter your username.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter(User.username == self.username.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        elif not user:
            self.username.errors.append("Invalid username")
        else:
            self.password.errors.append("Invalid password")
        return False


class SignupForm(Form):
    username = StringField("username", [validators.DataRequired("Please enter your username."), validators.length(4, 32,
                                                                                                                  "Your username must be between %(min)d and %(max)d characters")])
    firstname = StringField("First name", [validators.DataRequired("Please enter your first name.")])
    lastname = StringField("Last name", [validators.DataRequired("Please enter your last name.")])
    email = EmailField("Email", [validators.DataRequired("Please enter your email address."),
                                 validators.Email("Please enter your email address.")])
    group = HiddenField(u'Group', default='2')
    password = PasswordField('Password', [validators.DataRequired("Please enter a password."), validators.length(2, 12,
                                                                                                                 "Your password must be between %(min)d and %(max)d characters.")])
    bio = StringField('Bio', [])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        elif User.query.filter(User.username == str(self.username.data.lower())).first() is not None:
            self.username.errors.append("Username is already taken")
            return False
        elif User.query.filter(User.email == str(self.email.data.lower())).first() is not None:
            self.email.errors.append("E-mail is already taken")
            return False
        else:
            return True


class EditUserForm(Form):
    firstname = StringField("First name", [validators.DataRequired("Please enter your first name.")])
    lastname = StringField("Last name", [validators.DataRequired("Please enter your last name.")])
    email = EmailField("Email", [validators.DataRequired("Please enter your email address."),
                                 validators.Email("Please enter your email address.")])
    group = SelectField(u'Group', coerce=int)
    password = StringField('Password', [validators.DataRequired("Please enter a password."), validators.length(2, 12,
                                                                                                               "Your password must be between %(min)d and %(max)d characters.")])
    bio = StringField('Bio', [])
    submit = SubmitField("edit profile")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class IssueForm(Form):
    title = StringField("Title", [validators.DataRequired("Enter a title for the issue")])
    summary = StringField("Issue", [validators.DataRequired("Enter Your issue here")], widget=TextArea())

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class EditIssueForm(Form):
    title = StringField("Title", [validators.DataRequired("Enter a title for the issue")])
    summary = StringField("Issue", [validators.DataRequired("Enter Your issue here")], widget=TextArea())
    status = SelectField('type', choices=ISSUE_STATUS)
    assignee = SelectField(u'User', choices=ISSUE_ASSIGNEES)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
