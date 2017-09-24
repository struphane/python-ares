"""

"""

import os
import json

from ares.Lib import AresHtml
from ares.Lib import AresItem
from flask import render_template_string
from datetime import datetime


class Button(AresHtml.Html):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = button
  """
  alias, cssCls = 'button', 'btn btn-success'
  reference = 'https://www.w3schools.com/tags/tag_button.asp'

  def __str__(self):
    """ Return the String representation of HTML button """
    return '<button %s type="button" style="margin-bottom: 20px;margin-top: -10px;">%s</button>' % (self.strAttr(), self.vals)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.button("MyButton")

  def post(self, evenType, url, **kwargs):
    """
      Post method to get data directly by interacting with the page
      https://api.jquery.com/jquery.post/
    """
    # Part dedicated to run before the Ajax call
    jsData, pyData = [], []
    for key, data in kwargs.items():
      if key not in ('cssCls', 'js'):
        if issubclass(data.__class__, AresHtml.Html):
          jsData.append("%s: %s" % (key, data.val))
        else:
          pyData.append("%s='%s'" % (key, data))
    # Distinguish jsData (to be converted in the javascript layer) from python data
    # Python data will be converted on the server side and they will never change
    # on the client
    url = render_template_string('''{{ url_for(\'%s\', %s) }}''' % (url, ",".join(pyData)))
    preAjax = AresItem.Item("var %s = %s.html();" % (self.htmlId, self.jqId))
    preAjax.add(0, "%s.html('<i class=\"fa fa-spinner fa-spin\"></i> Processing'); " % self.jqId)
    preAjax.add(0, kwargs.get('preAjaxJs', ''))
    # Return the common post call method to a AresJs object
    super(Button, self).post(evenType, url, "{%s}" % ",".join(jsData),
                             '''
                              var res = JSON.parse(data) ;
                              var data = res.data ;
                              var status = res.status ;
                              %s.html(%s);
                              %s ;
                             ''' % (self.jqId, self.htmlId, kwargs.get('js', '')),
    str(preAjax), kwargs.get('redirectUrl', ''))


class ButtonRemove(AresHtml.Html):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-danger
    - glyphicon = remove
  """
  glyphicon, cssCls = 'remove', 'btn btn-danger'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'remove'

  def __str__(self):
    """ Return the String representation of a HTML Style Twitter button """
    return '<button type="button" %s><span class="fa fa-%s">&nbsp;%s</span></button>' % (self.strAttr(), self.glyphicon, self.vals)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.remove()


class ButtonDownload(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = download
  """
  glyphicon, cssCls = 'download', 'btn btn-success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'download'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.download()


class ButtonDownloadAll(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = downloadAll
  """
  glyphicon, cssCls = 'cloud-download', 'btn btn-success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'downloadAll'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.downloadAll()


class ButtonOk(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = ok
  """
  glyphicon, cssCls = 'check-square-o', 'success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'ok'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.ok("OK Button")


class ButtonRefresh(ButtonRemove):
  """
  Python wrapper to the HTML Button Refresh component

  """
  glyphicon, cssCls = 'refresh', 'btn btn-success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'refresh'

  def __init__(self, aresObj, vals, recordSet, ajaxScript, withDataFiles, cssCls=None):
    """
    Instantiate the object and attached the recordSet to the event
    This object will also store the data to a text file.
    """
    super(ButtonRefresh, self).__init__(aresObj, vals, cssCls)
    self.ajaxScript = ajaxScript
    self.dataFileName = "%s.json" % id(recordSet)
    if withDataFiles:
      dataPath = os.path.join(aresObj.http['DIRECTORY'], 'data')
      if not os.path.exists(dataPath):
        os.makedirs(dataPath)
      recordSetJson = open(os.path.join(dataPath, self.dataFileName), "w")
      json.dump(recordSet, recordSetJson)
      recordSetJson.close()

  def click(self, jsFnc, vars=None):
    """
    Add the corresponding event when the button is clicked

    """
    jsVars, pyVars = set(), set()
    if vars is not None:
      for key, val in vars.items():
        if issubclass(val.__class__, AresHtml.Html):
          # In this case we cannot have the parameters hard coded
          # So we need to use Javascript and the Ajax Get and Post features to deduce it on the fly
          jsVars.add("%s=' + %s" % (key, val.val))
        else:
          pyVars.add("%s='%s'" % (key, val))
    if 'report_name' not in pyVars:
      pyVars.add("report_name='%s'" % self.aresObj.http['REPORT_NAME'])
    if 'script' not in pyVars:
      pyVars.add("script='%s'" % self.ajaxScript)
    if 'file_name' not in pyVars:
      pyVars.add("file_name='%s'" % self.dataFileName)
    if 'user_script' not in pyVars:
      pyVars.add("user_script='%s'" % self.aresObj.http.get('USER_SCRIPT', self.aresObj.http['REPORT_NAME']))

    strUrl = render_template_string('''{{ url_for('ares.ajaxCall', %s) }}''' % ",".join(pyVars))
    if "?" in strUrl and jsVars:
      strUrl = "'%s&amp;%s" % (strUrl, " + '&amp;".join(jsVars))
    print strUrl

    self.js('click',
            render_template_string('''
                // The first part will update the file
                $.post(%s, function(result) {
                    var res = JSON.parse(result) ;
                    var data = res.data ;
                    var status = res.status ;
                    // Then it will update the reports
                    %s
                });
              ''' % (strUrl, jsFnc)
            ))

  def __str__(self):
    """ Return the String representation of a HTML Style Twitter button """
    return '<button type="button" %s style="margin-bottom: 20px;margin-top: -10px;"><span class="fa fa-%s">&nbsp;%s</span></button>' % (self.strAttr(), self.glyphicon, self.vals)


class GeneratePdf(ButtonRemove):
  alias = "generatePdf"
  glyphicon, cssCls = "book", "btn btn-default"
  source = r"http://pdfmake.org/#/gettingstarted"

  def __init__(self, aresObj, fileName=None, cssCls=None): # Hack: I need the whole aresObj as param since I need to retrieve everything that has been created so far
    super(GeneratePdf, self).__init__(aresObj, "", cssCls)

    if fileName is None:
      fileName = "%s_%s" % (aresObj.reportName.strip().replace(" ", "_") if hasattr(aresObj, "reportName") else "ares_export", datetime.now())

    content = []
    styles = {"Title": {"fontSize": 22, "bold": "true", "italic": "true", "alignment": "left"}}
    for objId in aresObj.content:
      htmlObj = aresObj.htmlItems[objId]
      content.append({"text": htmlObj.vals, "style": htmlObj.__class__.__name__})
    varName = "%s_Content" % self.htmlId
    varTxt = "var %s = %s;" % (varName, json.dumps({"content": content, "style": styles}))

    """
    var generatepdf_2_Content = {content: [{text: 'Mrflex Monitoring', style: 'Title'}],
                             styles: {Title: {fontSize: 40, bold: true, italic: true}}};

      $("#generatepdf_2").on("click", function(event)
      {
          pdfMake.createPdf(generatepdf_2_Content).download('Mrflex_Monitoring_2017-08-24 23:28:20.011011.pdf');
      }
      );
    """
    self.jsEvent["var"] = varTxt#"var docDefinition = { content: 'This is an sample PDF printed with pdfMake' };"
    self.jsEvent["click"] = AresJs.JQueryEvents(self.htmlId, '$("#%s")' % self.htmlId, "click", "pdfMake.createPdf(%s).download('%s.pdf');" % (varName, fileName))
