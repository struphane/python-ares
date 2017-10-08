""" Wrapper for the flask environment

"""

from __future__ import print_function
import AresInstall
import re

def render_template_string(val):
  """ Wrap the function to convert the URL """
  res = re.findall('<link rel="stylesheet" href="{{ url_for\(\'static\',filename=\'css/([a-zA-Z0-9-.]*)\'\) }}" type="text/css">', val)
  if res:
    resolvedCss = ['<link rel="stylesheet" href="%s/static/css/%s" type="text/css">' % (AresInstall.SERVER_PATH, val.replace("\\", "/")) for val in res]
    return "\n".join(resolvedCss)

  res = re.findall('<script language="javascript" type="text/javascript" src="{{ url_for\(\'static\',filename=\'js/([a-zA-Z0-9-.]*)\'\) }}"></script>', val)
  if res:
    resolvedJs = ['<script language="javascript" type="text/javascript" src="%s/static/js/%s"></script>' % (AresInstall.SERVER_PATH, val.replace("\\", "/")) for val in res]
    return "\n".join(resolvedJs)

  return val