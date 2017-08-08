""" Special app for the report section

"""

import os

from flask import Flask
app = Flask(__name__)
app.config['ROOT_PATH'] = os.path.dirname(os.path.abspath(__file__))

from ares.report import report
app.register_blueprint(report)

if __name__ == "__main__":
    app.debug = True
    app.run()