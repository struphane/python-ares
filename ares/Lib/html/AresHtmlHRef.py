""" Module dedicate to produce the Link to different pages

In this module ze use Jinja to convert the url alias to the proper one.
This will help users to not care about the path but rather to focus on the parameters to be paased.

Classes are generic and use kwargs to get all the possible paramaters
cssCls is also passed in the args

"""

from ares.Lib import AresHtml

from flask import render_template_string


class A(AresHtml.Html):
  """
  Class to link a script to another sub script in a report
  In this class no Javascript is used in the click event
  """
  alias, cssCls = 'anchor', 'btn btn-success'
  flask = 'ares.run_report'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['jquery']

  def __init__(self, aresObj, vals, **kwargs):
    super(A, self).__init__(aresObj, vals, kwargs.get('cssCls'))
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
                var baseUrl = "{{ url_for(\'%s\', %s ) }}";
                if (baseUrl.indexOf("?") !== -1) { var ullUrl = baseUrl + "&" + %s ; }
                else { var ullUrl = baseUrl + "?" + %s ; }
                window.location.href = ullUrl ;
            }
          ) ;
        ''' % (self.jqId, self.flask, ",".join(values), "+ '&' +".join(jsData), "+ '&' +".join(jsData)), **self.kwargs)
      return '<a href="#" %s>%s</a>' % (self.strAttr(), self.vals)

    return render_template_string('<a %s href="{{ url_for(\'%s\', %s ) }}">%s</a>' % (self.strAttr(), self.flask, ",".join(values), self.vals), **self.kwargs)


class ScriptPage(A):
  """
  Class to link a script to another sub script in a report
  In this class no Javascript is used in the click event
  """
  alias, cssCls = 'main', ''
  flask = 'ares.run_report'
  reqCss = ['bootstrap']
  reqJs = ['jquery']


class Download(A):
  """

  """
  alias, cssCls = 'anchor_download', 'fa fa-download'
  flask = 'ares.downloadFiles'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['jquery']


class CreateEnv(A):
  """

  """
  alias, cssCls = 'anchor_set_env', 'btn btn-primary'
  flask = 'ares.ajaxCreate'
  reqCss = ['bootstrap']
  reqJs = ['jquery']


class AddScript(A):
  """ """
  alias, cssCls = 'anchor_add_scripts', 'btn btn-primary'
  flask = 'ares.addScripts'
  reqCss = ['bootstrap']
  reqJs = ['jquery']


class ABespoke(AresHtml.Html):
  """
  Class to link a script to another sub script in a report
  In this class no Javascript is used in the click event
  """
  alias, cssCls = 'external_link', ''
  reqCss = ['bootstrap']
  reqJs = ['jquery']

  def __init__(self, aresObj, vals, url, **kwargs):
    super(ABespoke, self).__init__(aresObj, vals, kwargs.get('cssCls'))
    self.url = url

  def __str__(self):
    """ Standard string representation for a href """
    return '<a %s href="%s" target="_blank">%s</a>' % (self.strAttr(), self.url, self.vals)
