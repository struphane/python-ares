from __future__ import print_function
import AresInstall
import re

def render_template_string(val):
  """ Wrap the function to convert the URL """
  res = re.search('<link rel="stylesheet" href="{{ url_for\(\'static\',filename=\'css/([a-zA-Z0-9.]*)\'\) }}" type="text/css">', val)
  if res is not None:
	  return "%s/static/css/%s" % (AresInstall.SERVER_PATH, res.group(1).replace("\\", "/"))

  return val