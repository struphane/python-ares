""" Python Wrapper for the Radio items
@author: Olivier Nogues

"""

import json

from ares.Lib import AresHtml
from ares.Lib import AresItem
from flask import render_template_string


class Radio(AresHtml.Html):
  """

  """
  alias, cssCls = 'radio', None
  references = ['https://www.w3schools.com/bootstrap/bootstrap_forms_inputs.asp']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, recordSet, col=None, cssCls=None, cssAttr=None, internalRef=None, checked=None):
    """ Instantiate a Python Radio button """
    if col is not None:
      vals = set([])
      for rec in recordSet:
        if col in rec:
          vals.add(rec[col])
    else:
      vals = set(recordSet)
    super(Radio, self).__init__(aresObj, list(vals), cssCls, cssAttr)
    self.col = col
    self.internalRef = internalRef
    self.checked = checked

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    if self.internalRef is not None:
      return self.internalRef

    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  def __str__(self):
    """ Return a basic HTML radio component """
    item = ['<div %s class="btn-group" data-toggle="buttons">' % self.strAttr(False)]
    for val in self.vals:
      if self.checked == val:
        item.append('<label class="btn btn-success active" name="%s">' % self.htmlId)
        item.append('%s<input type="radio" name="input_%s" value="%s" checked="checked" autocomplete="off">' % (val, self.htmlId, val))
      else:
        item.append('<label class="btn btn-info" name="%s">' % self.htmlId)
        item.append('%s<input type="radio" name="input_%s" value="%s" autocomplete="off">' % (val, self.htmlId, val))
      item.append('<span class="awesomeicon fa fa-check">&nbsp;</span></label></div>')
    return "".join(item)

  @property
  def jqId(self):
    """
    Property to get the Jquery ID of a python HTML object
    The use of ' instead of " is because the dumps will add some \ and it will not be correctly taken into account
    by the javascript layer
    """
    return "$('label[name=%s]')" % self.htmlId

  @property
  def jqIdChecked(self):
    """ Special property for radio button which adds the checked attribute"""
    return  "$('input[name=input_%s]:checked') " % self.htmlId

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    #return "radio_val_%s" % self.htmlId
    return "$('input[name=input_%s]:checked').val()" % self.htmlId

  def post(self, evenType, scriptName, jsDef, attr):
    """ Button Post request """
    url = render_template_string('''{{ url_for(\'ares.ajaxCall\', report_name=\'%s\', script=\'%s\') }}''' % (
    self.aresObj.http['REPORT_NAME'], scriptName))
    data = json.dumps(attr, cls=AresHtml.SetEncoder)
    for stToConv in ['.data().toArray()', '.val()', '.serializeArray()']:
      data = data.replace('%s"' % stToConv, stToConv)
    for stToConv, strReplace in [('$(', '"$('), (': datatable_', ': "datatable_')]:
      data = data.replace(strReplace, stToConv)
    jsDef = '''
              %s
              var postData = %s;
              postData['btnValue'] = radio_val_%s;
              $.post("%s", postData, function(data) {
                  var res = JSON.parse(data) ;
                  var data = res.data ;
                  var status = res.status ;
              } ); 
            ''' % (jsDef, data, self.htmlId, url)
    self.js(evenType, jsDef, url=url)

  def jsFnc(self, js):
    """ Pure Javascript method to update other components in the page """
    self.js('mouseup', "radio_val_%s = $(event.currentTarget).text().trim(); %s" % (self.htmlId, js))

  def click(self, htmlObjects):
    """ Pure Javascript method to update other components in the page """
    evenType = 'mouseup'
    jsDef = [] #["radio_val_%s = $(event.currentTarget).text().trim();" % self.htmlId]
    for htmlObject in htmlObjects:
      jsDef.append(htmlObject.jsUpdate())
    self.js(evenType, "\n".join(jsDef))

  def clickWithPost(self, scriptName, attr=None):
    """ """
    attr = {} if attr is None else attr
    jsDef = "radio_val_%s = $(event.currentTarget).text().trim();" % self.htmlId
    self.post('click', scriptName, jsDef, attr)

  def link(self, jsEvent):
    """ Change the component to use javascript functions """
    jsFrg = list(self.jsFrg)
    jsFrg.append(jsEvent)
    self.js('mouseup', ";".join(jsFrg))