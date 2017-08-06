""" Special app for the report section

"""

import os

from flask import Blueprint, Flask, render_template, request, send_from_directory, send_file
app = Flask(__name__)
app.config['ROOT_PATH'] = os.path.dirname(os.path.abspath(__file__))

from views.report import report
app.register_blueprint(report)

#report = Blueprint('ares', __name__)
#app.register_blueprint(report) #, url_prefix='/pages')

#app.config['ARES_FOLDER'] = 'ares'
#app.config['ARES_USERS_LOCATION'] = 'user_reports'

#print(app.config['APPLICATION_ROOT'])

if __name__ == "__main__":
    app.debug = True
    app.run()