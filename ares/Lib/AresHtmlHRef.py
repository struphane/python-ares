""" Module dedicate to produce the Link to different pages

In this module ze use Jinja to convert the url alias to the proper one.
This will help users to not care about the path but rather to focus on the parameters to be paased.

Classes are generic and use kwargs to get all the possible paramaters
cssCls is also passed in the args

"""

from ares.Lib import AresHtml

from flask import render_template_string


class Script(AresHtml.Html):
  """
  Class to link a script to another sub script in a report
  In this class no Javascript is used in the click event
  """
  alias, cssCls = 'script', 'btn btn-success'

  def __init__(self, htmlId, vals, **kwargs):
    super(Script, self).__init__(htmlId, vals, kwargs.get('cssCls'))
    self.kwargs = kwargs

  def __str__(self):
    """ Return the String representation of a Anchor HTML object """
    values, needJs, jsData = [], False, []
    for key, data in self.kwargs.items():
      if key not in ('cssCls', ):
        if issubclass(data.__class__, AresHtml.Html):
          # In this case we cannot have the parameters hard coded
          # So we need to use Javascript and the Ajax Get and Post features to deduce it on the fly
          jsData.append("'%s=' + %s" % (key, data.val))
          needJs = True

        else:
          values.append("%s='%s'" % (key, data))

    if needJs:
      self.jsEvent['click'] = render_template_string(
        '''
          %s.on("click", function (event){  
                var baseUrl = "{{ url_for(\'ares.launch\', %s ) }}";
                var ullUrl = baseUrl + "?" + %s ;
                window.location.href = ullUrl ;
            }
          ) ;
        ''' % (self.jqId, ",".join(values), "&".join(jsData)),
        **self.kwargs)

      return '<a href="#" %s>%s</a>' % (self.strAttr(), self.vals)

    return render_template_string('<a %s href="{{ url_for(\'ares.launch\', %s ) }}">%s</a>' % (self.strAttr(), ",".join(values), self.vals), **self.kwargs)
