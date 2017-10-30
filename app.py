""" Special app for the report section

"""

import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
import config
# from system.sqlite.db_config import models

app = Flask(__name__)
app.config['ROOT_PATH'] = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///%s' % os.path.join(app.config['ROOT_PATH'], 'system', 'sqlite', 'main_sqlite.db')
print(app.config['SQLALCHEMY_DATABASE_URI'])
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
  email = db.Column(db.String(120), primary_key=True, unique=True)
  password = db.Column(db.String(80))

  def __init__(self, email, password):
    self.email = email
    self.password = password

  def __repr__(self):
    return '<User %r>' % self.email

  def get_id(self):
    """ """
    return self.email

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

with app.app_context():
    from ares.report import report
    app.register_blueprint(report)

from saturn.saturn import saturn
app.register_blueprint(saturn)
