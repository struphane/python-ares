""" Special app for the report section

"""

import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
import config
import hashlib
from Libs import AresUserAuthorization
# from system.sqlite.db_config import models

app = Flask(__name__)
app.config['ROOT_PATH'] = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///%s' % os.path.join(app.config['ROOT_PATH'], 'system', 'sqlite', 'main_sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# POSTGRES = {
#     'user': 'postgres',
#     'pw': '240985',
#     'db': 'risklab',
#     'host': 'localhost',
#     'port': '5432',
# }

app.config['SECRET_KEY'] = 'K3y2BCh4ng3d'#Change this if you want the app to work


login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
  uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  team_name = db.Column(db.String(120), db.ForeignKey('team.team_name'), nullable=False)
  password = db.Column(db.String(80), nullable=False)
  team_confirm = db.Column(db.String(1), default='N')
  datasources = db.relationship('DataSource')
  environments = db.relationship('EnvironmentDesc')

  def __init__(self, email, team, password):
    self.email = email
    self.team_name = team
    self.password = hashlib.sha256(bytes(password.encode('utf-8'))).hexdigest()

  def __repr__(self):
    return '<User %r>' % self.email

  def get_id(self):
    """ """
    return self.email

class Team(db.Model):

  __tablename__ = 'team'

  team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  team_name = db.Column(db.String(120), nullable=False, unique=True)
  team_email = db.Column(db.String(120), nullable=False, unique=True)
  team_approvals = db.relationship('TeamApproval')

  def __init__(self, team_name, email):
    self.team_name = team_name
    self.team_email = email

class DataSource(db.Model):
  """ """
  __tablename__ = 'datasource'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  source_name = db.Column(db.String(20), nullable=False)
  uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
  source_username = db.Column(db.String(120), nullable=False)
  source_pwd = db.Column(db.String(120))
  salt = db.Column(db.Integer, nullable=False)

  __table_args__ = (db.UniqueConstraint('source_name', 'uid', name='uix_1'), )

  def __init__(self, source_name, uid, source_username, source_pwd, salt):
    """ """
    self.source_name = source_name
    self.uid = uid
    self.source_username = source_username
    self.source_pwd = source_pwd
    self.salt = salt

class TeamApproval(db.Model):
  """ """
  __tablename__ = 'table_approve'

  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
  username = db.Column(db.String(120),  nullable=False)

  __table_args__ = (db.UniqueConstraint('team_id', 'username', name='uix_2'), )

  def __init__(self, team_id, username):
    """ """
    self.team_id = team_id
    self.username = username


class EnvironmentDesc(db.Model):
  __tablename__ = 'env_dsc'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  env_name = db.Column(db.String(20), nullable=False)
  team_name = db.Column(db.String(120), db.ForeignKey('user.team_name'), nullable=False)

  def __init__(self, env_name, team_name):
    """ """
    self.env_name = env_name
    self.team_name = team_name


def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

login_manager = LoginManager()
with app.app_context():
  login_manager.init_app(app)
  login_manager.login_view = 'ares.aresLogin'
  from ares.report import report
  app.register_blueprint(report)

from saturn.saturn import saturn
app.register_blueprint(saturn)
