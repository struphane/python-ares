""" Special app for the report section

"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config['ROOT_PATH'] = os.path.dirname(os.path.abspath(__file__))

POSTGRES = {
    'user': 'postgres',
    'pw': '240985',
    'db': 'risklab',
    'host': 'localhost',
    'port': '5432',
}

if config.ARES_MODE == 'LIVE':
    from system.sqlite.db_config import setup_db_env
    setup_db_env.launch_db(app.config['ROOT_PATH'])


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


from ares.report import report
app.register_blueprint(report)

from saturn.saturn import saturn
app.register_blueprint(saturn)
