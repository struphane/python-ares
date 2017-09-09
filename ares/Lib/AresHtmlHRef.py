""" Module dedicate to produce the Link to different pages

In this module ze use Jinja to convert the url alias to the proper one.
This will help users to not care about the path but rather to focus on the parameters to be paased.

Classes are generic and use kwargs to get all the possible paramaters
cssCls is also passed in the args

"""

from ares.Lib import AresHtml

from flask import render_template_string


class Child(AresHtml.Html):
  """
  Class to link a script to another sub script in a report
  In this class no Javascript is used in the click event
  """
  alias = 'child'

  def __init__(self, htmlId, vals, **kwargs):
    super(Child, self).__init__(htmlId, vals, kwargs.get('cssCls'))
    self.kwargs = kwargs

  def __str__(self):
    """ Return the String representation of a Anchor HTML object """
    return render_template_string('<a href="{{ url_for(\'ares.run_report\', report_name=\'%s\') }}">%s</a>' % (self.kwargs.get('report_name'), self.vals), **self.kwargs)
