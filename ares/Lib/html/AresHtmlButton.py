"""
Definition of all the different HTML button wrappers.
From this module lot of different sort of HTML buttons can be displayed like:
  - ButtonDownload, the button dedicated to download files
  - ButtonRefresh, the button dedicated to query another script in the framework and then to refresh data
  - ButtonOk, to validate something and return a notification
  - GeneratePdf, to generate a Pdf report

Also it is possible to use the generic and basic button object - Button - to then change it to a specific one in your report.
Some based functions are available in order to change more or less everything in the python
"""

import os
import json
from datetime import datetime

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

from flask import render_template_string


class Button(AresHtml.Html):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = button
  """
  alias, cssCls = 'button', ['btn', 'btn-success']
  references = ['https://www.w3schools.com/tags/tag_button.asp',
                'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']
  css = {'margin-bottom': '20p', 'margin-top': '-10p'}

  def __init__(self, aresObj, vals, cssCls, cssAttr, awsIcon):
    """  Instantiate the object and store the icon """
    super(Button, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.awsIcon = awsIcon

  def __str__(self):
    """ Return the String representation of HTML button """
    if self.awsIcon is not None:
      return '<button type="button" %s><span class="fa fa-%s">&nbsp;%s</span></button>' % (self.strAttr(), self.awsIcon, self.vals)

    return '<button %s>%s</button>' % (self.strAttr(), self.vals)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.button("MyButton")

  def post(self, evenType, scriptName, jsDef, attr):
    """

    """
    url = render_template_string('''{{ url_for(\'ares.ajaxCall\', report_name=\'%s\', script=\'%s\') }}''' % (self.aresObj.http['REPORT_NAME'], scriptName))
    data = json.dumps(attr, cls=AresHtml.SetEncoder).replace('"$(', '$(').replace('.val()"', '.val()')
    preAjax = AresItem.Item("var %s = %s.html();" % (self.htmlId, self.jqId))
    preAjax.add(0, "%s.html('<i class=\"fa fa-spinner fa-spin\"></i> Processing'); " % self.jqId)
    preAjax.add(0, attr.get('preAjaxJs', ''))
    jsDef = '''
              %s
              $.post("%s", %s, function(data) {
                  var res = JSON.parse(data) ;
                  var data = res.data ;
                  var status = res.status ;
                  %s
                  %s.html(%s);
              } );
            ''' % (preAjax, url, data, jsDef, self.jqId, self.htmlId)
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType,jsDef, url=url)

  def click(self, scriptName, jsDef, attr):
    """ Implement the click event on the button object """
    self.post('click', scriptName, jsDef, attr)


class ButtonRefresh(AresHtml.Html):
  """
  Python wrapper to the HTML Button Refresh component

  """
  glyphicon, cssCls = 'refresh', ['btn', 'btn-success']
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'refresh'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

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
      strUrl = "%s&amp;%s +'" % (strUrl, " + '&amp;".join(jsVars))
    self.js('click',
            render_template_string('''
                // The first part will update the file
                $.post('%s', function(result) {
                    var res = JSON.parse(result) ;
                    var data = res.data ;
                    var status = res.status ;
                    if (status == 'Error') {
                      alert(res.message) ;
                    }
                    else {
                      // Then it will update the reports
                      %s
                    }
                });
              ''' % (strUrl, jsFnc)
            ))

  def __str__(self):
    """ Return the String representation of a HTML Style Twitter button """
    return '<button type="button" %s style="margin-bottom: 20px;margin-top: -10px;"><span class="fa fa-%s">&nbsp;%s</span></button>' % (self.strAttr(), self.glyphicon, self.vals)


class ButtonDownload(Button):
  """ """
  alias = "download"
  glyphicon, cssCls = "download", ['btn', 'btn-default']
  reqCss = ['bootstrap', 'font-awesome']

  def __init__(self, aresObj, vals, reportName, cssCls=None, cssAttr=None, awsIcon=None):
    """ """
    super(ButtonDownload, self).__init__(aresObj, vals, cssCls, cssAttr, awsIcon)
    self.reportName = reportName

  def __str__(self):
    """ """
    items = AresItem.Item('<button type="button" %s>' % self.strAttr())
    items.add(1, render_template_string('<a href="{{ url_for(\'ares.downloadOutputs\', report_name=\'%s\', file_name=\'%s\') }}" download />' % (self.reportName, self.vals)))
    items.add(0, 'Download</button>')
    return str(items)


class GeneratePdf(AresHtml.Html):
  alias = "generatePdf"
  glyphicon, cssCls = "book", ['btn', 'btn-default']
  source = r"http://pdfmake.org/#/gettingstarted"
  reqJs = ['pdfmake']

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
