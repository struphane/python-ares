"""

"""

from ares.Lib import AresHtml
from flask import render_template_string


class Image(AresHtml.Html):
  """
  Python wrapper for a multi Tabs component

  Default class parameters
    - CSS Default Class = nav nav-tabs
    - title = Home
  """
  alias =  'img'
  cssCls = ['img-responsive']
  references = ['https://www.w3schools.com/bootstrap/bootstrap_ref_css_images.asp',
                'https://www.w3schools.com/cssref/css3_pr_border-radius.asp']
  doubleDots = 1
  __css = {'border': '1px solid grey',  'border-radius': '15px;', "margin-bottom": "15px",
           'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'}

  def __str__(self):
    """ Return the HTML representation of a Tabular object """
    return render_template_string('<img src="{{ url_for(\'static\',filename=\'images/%s\') }}" style="width:100%%;max-width:700px;" %s> ' % (self.vals, self.strAttr()))
