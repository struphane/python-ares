""" Special app for the report section

"""

import os
import config

from flask import current_app, Blueprint, Flask, render_template, request, send_from_directory, send_file

# Ares Framework
from ares.Lib import Ares

saturn = Blueprint('saturn', __name__, url_prefix='/saturn')

# Return the list of all the scripts needed to run this package
# This will group all the module CSS, JS and Python scripts
LIB_PACKAGE = {
  'JS': ['jquery-3.2.1.min.js', 'jquery-ui.min.js', 'bootstrap.min.js', 'bootstrap-select.min.js', 'd3.v3.js',
         'nv.d3.js', 'd3.layout.cloud.js'],
  'CSS': ['jquery-ui.css', 'bootstrap.min.css', 'bootstrap-theme.min.css', 'nv.d3.css',
          'bootstrap-select.min.css', 'w3.css'],
  'PY': ['Ares.py', 'AresGraph.py', 'AresHtml.py', 'AresJs.py', '__init__.py'],
  'JSON': ['horizBars.json', 'linePlusBarData.json', 'lineWithFocus.json', 'multiBar.json', 'stackedAreaData.json']
}

@saturn.route("/")
@saturn.route("/index")
def index():
  """ Return the main page with the reports selection """
  aresObj = Ares.Report()
  aresObj.title(1, 'test')
  return render_template('ares_template.html', content=aresObj.html(None))
