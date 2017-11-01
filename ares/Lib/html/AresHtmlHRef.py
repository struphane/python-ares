""" Module dedicate to produce the Link to different pages

In this module ze use Jinja to convert the url alias to the proper one.
This will help users to not care about the path but rather to focus on the parameters to be paased.

Classes are generic and use kwargs to get all the possible paramaters
cssCls is also passed in the args

"""

import json
from ares.Lib import AresHtml
from ares.Lib import AresJs
from flask import render_template_string


class ExternalLink(AresHtml.Html):
  """ To display a reference to an external website """
  alias, cssCls = 'externalLink', None
  references = ['https://www.w3schools.com/TagS/att_a_href.asp']

  def __init__(self, aresObj, vals, url, cssCls, cssAttr):
    """ The URL has to be mentioned """
    super(ExternalLink, self).__init__(aresObj, vals,  cssCls, cssAttr)
    self.url = url

  def __str__(self):
    """ Return the HTML representation of the hyperlink object """
    if self.vals is None:
      return '<a href="%s" %s target="_blank">%s</a>' % (self.url, self.strAttr(), self.url)

    return '<a href="%s" %s target="_blank">%s</a>' % (self.url, self.strAttr(), self.vals)


class Download(AresHtml.Html):
  """

  """
  alias, cssCls = 'anchor_download', ['fa fa-download']
  flask = 'ares.downloadFiles'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['jquery']

  def __init__(self, aresObj, vals, attrs, cssCls, cssAttr):
    super(A, self).__init__(aresObj, vals,  cssCls, cssAttr)
    self.getData = attrs if attrs is not None else {} # Special attributes to add to the URL
    if not 'REPORT_NAME' in self.getData:
      self.getData['REPORT_NAME'] = self.aresObj.http['REPORT_NAME']
    if not 'SCRIPT_NAME' in self.getData:
      self.getData['SCRIPT_NAME'] = self.aresObj.http['REPORT_NAME']

  def resolve(self):
    """ Use Flak modules to translave the URL from the function name """
    url = render_template_string('''{{ url_for(\'ares.downloadFiles\', report_name=\'%(REPORT_NAME)s\', script_name=\'%(SCRIPT_NAME)s\') }}''' % self.getData)
    return url

  def __str__(self):
    """ Return the String representation of a Anchor HTML object """
    url = self.resolve()
    if len(self.getData) < 3:
      return '<a href="%s" %s>%s</a>' % (url, self.strAttr(), self.vals)

    data = json.dumps(self.getData, cls=AresHtml.SetEncoder).replace('"$(', '$(').replace('.val()"', '.val()')
    jsDef = '''
              %s.on("click", function (event){
                var baseUrl = "%s";
                if (baseUrl.indexOf("?") !== -1) { var ullUrl = baseUrl + "&" + %s ; }
                else { var ullUrl = baseUrl + "?" + %s ; }
                window.location.href = ullUrl ;
              }
            ) ;
            ''' % (self.jqId, url, data, data)
    self.get('click', url, data, '')
    #self.aresObj.jsOnLoadFnc.add(jsDef)
    return '<a href="#" %s>%s</a>' % (self.strAttr(), self.vals)


class InternalLink(AresHtml.Html):
  """
  Class to link a script to another sub script in a report
  In this class no Javascript is used in the click event
  """
  alias, cssCls = 'anchor', ['btn', 'btn-success']
  flask = 'ares.run_report'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['jquery']

  def __init__(self, aresObj, linkValue, script, attrs, cssCls, cssAttr):
    super(InternalLink, self).__init__(aresObj, linkValue,  cssCls, cssAttr)
    self.getData = attrs if attrs is not None else {} # Special attributes to add to the URL
    if not 'REPORT_NAME' in self.getData:
      self.getData['REPORT_NAME'] = self.aresObj.http['REPORT_NAME']
    self.getData['SCRIPT_NAME'] = script

  def resolve(self):
    """ Use Flak modules to translave the URL from the function name """
    url = render_template_string('''{{ url_for(\'ares.run_report\', report_name=\'%(REPORT_NAME)s\', script_name=\'%(SCRIPT_NAME)s\') }}''' % self.getData)
    return url

  def __str__(self):
    """ Return the String representation of a Anchor HTML object """
    url = self.resolve()
    if len(self.getData) < 3:
      return '<a href="%s" %s>%s</a>' % (url, self.strAttr(), self.vals)

    data = json.dumps(self.getData, cls=AresHtml.SetEncoder).replace('"$(', '$(').replace('.val()"', '.val()')
    jsDef = '''
                var baseUrl = "%s";
                var data = %s;
                var params = "";
                for (key in data) {
                  if (!(key == 'REPORT_NAME') && !(key == 'SCRIPT_NAME')) {
                    params = params + '&' + key + '=' + data[key];
                  }
                }
                params = params.substr(1); // remove the first &
                if (baseUrl.indexOf("?") !== -1) { var ullUrl = baseUrl + "&" + params ; }
                else { var ullUrl = baseUrl + "?" + params ; }
                window.location.href = ullUrl ;
            ''' % (url, data)
    self.js('click', jsDef)
    return '<a href="#" %s>%s</a>' % (self.strAttr(), self.vals)