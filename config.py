import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = False
SECRET_KEY = 'It-is-a-secret'

COMPANY_NAME = 'Vuln Corp'

SQLALCHEMY_TRACK_MODIFICATIONS = False
