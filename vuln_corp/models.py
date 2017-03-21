import datetime

from vuln_corp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    picture = db.Column(db.String(64))
    password = db.Column(db.String(32), unique=False)
    group = db.Column(db.Integer)
    email = db.Column(db.String(64), unique=True)
    creation_date = db.Column(db.DateTime)

    def __init__(self, username, firstname, lastname, email, password, group):
        self.username = username.lower()
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.password = password
        self.group = group
        self.picture = 'static/default.jpg'
        self.creation_date = datetime.datetime.now()

    def check_password(self, password):
        return password == self.password

    def get_fullname(self):
        return str(self.firstname) + ' ' + str(self.lastname)

    def get_group(self):
        return Groups.query.filter(Groups.id == self.group).first().groupname

    def get_groupid(self, id):
        return Groups.query.filter(Groups.id == id).first().groupname

    def exists(self):
        if self.username == User.query.filter(User.username == self.username).first().data():
            return True
        else:
            return False

    def get_session(self):
        return Session.query.filter(Session.username == self.username).first()

    def __repr__(self):
        return '<Username:{} Password:{}>'.format(self.username, self.password)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), db.ForeignKey('user.username'))
    session_id = db.Column(db.String(32), unique=True)
    active = db.Column(db.Boolean)

    def __init__(self, username, session_id, active):
        self.username = username
        self.session_id = session_id
        self.active = active

    def get_user(self):
        return User.query.filter(User.username == self.username).first()

    def __repr__(self):
        return '<User:{} session_id:{} active:{}>'.format(self.username, self.session_id, self.active)


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), unique=True)

    def __init__(self, groupname):
        self.groupname = groupname

    def __repr__(self):
        return '<group:{}>'.format(self.groupname)
