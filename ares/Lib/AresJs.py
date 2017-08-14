""" Python Wrapper for Pure javascript call

This will be the helper for the Ajax calls

This module require jQuery
reference website: http://api.jquery.com/jquery.ajax/

"""

from ares.Lib import AresItem

class JQueryEvents(object):
  """

  """
  mapEvent = {'drop': ['%(src)s.on("%(eventType)s", function (event){', '}', ');'],
              'dragover': ['%(src)s.on("%(eventType)s", function (event){', '}', ');'],
              'dragleave': ['%(src)s.on("%(eventType)s", function (event){', '}', ');'],
              'dragenter': ['%(src)s.on("%(eventType)s", function (event){', '}', ');'],
              'click': ['%(src)s.on("%(eventType)s", function (event){', '}', ');'],
              'blur': [''],
              'autocomplete': ['%(src)s.autocomplete({', '}', ');'],
              'change': ['%(src)s.on("%(eventType)s", function (event){', '}', ');'],
        }

  def __init__(self, htmlId, jsSrcRef, eventType, jsFnc, data=None, url=None):
    """
    """
    if not eventType in self.mapEvent:
      # This is a check to control the number of events per class
      # Also because some of them might require specific display
      print('Do not use any Ajax call or bespoke methods here')
      print('In the function is not implemented yet please have a look at the call in AreHtml.py')
      raise Exception('%s not defined for this %s!' % (eventType, self.__class__))

    if isinstance(jsFnc, str):
      splitFnc = jsFnc.strip().split("\n")
      items = AresItem.Item(splitFnc[0].strip())
      for line in splitFnc[1:]:
        items.add(0, line.strip())
      jsItemFnc = items
    else:
      jsItemFnc = jsFnc
    self.jsAttr = {'src': jsSrcRef, 'eventType': eventType, 'fnc': jsItemFnc, 'htmlId': htmlId,
                   'data': data, 'url': url}

  def __repr__(self):
    """  Return the String representation of the Javascripts methods """
    self.jsAttr['fnc'].incIndent = 2
    jsFnc = str(self.jsAttr['fnc'])[1:] # remove the empty line at the top
    eventDefinition = self.mapEvent[self.jsAttr['eventType']]
    items = AresItem.Item(eventDefinition[0] % self.jsAttr)
    if '%(' in jsFnc:
      items.add(0, jsFnc % self.jsAttr['eventType'])
    else:
      items.add(0, jsFnc)
    for i, strEvent in enumerate(eventDefinition[1:]):
      items.add(len(eventDefinition) - i - 1, strEvent)
    return str(items)


class JD3Graph(object):
  """

  jGraphAttr = {'src': self.jsRef(), 'fnc': jsDef, 'htmlId': self.htmlId}
  """

  def __init__(self, jGraphAttr, chart, data):
    """ """
    self.jGraphAttr = jGraphAttr

    if isinstance(chart, str):
      splitFnc = chart.strip().split("\n")
      items = AresItem.Item(splitFnc[0].strip())
      items.incIndent = 2
      for line in splitFnc[1:]:
        items.add(0, line.strip())
      jsChart = items
    else:
      jsChart = chart

    self.jGraphAttr.update({'chart': str(jsChart)[1:].strip(), 'data': data})

  def __repr__(self):
    """ """
    res = AresItem.Item()
    res.add(1, 'var chart_%(htmlId)s = %(chart)s' % self.jGraphAttr)
    res.add(1, "var data_%(htmlId)s = %(data)s ;" % self.jGraphAttr)
    res.add(1, "d3.%(src)s.datum(data_%(htmlId)s).transition().call(chart_%(htmlId)s) ; " % self.jGraphAttr)
    return str(res)




def genericCall(url, method, data, success, fail):
    """ Generic Ajax callback method """
    return '''
              $.ajax({
                    url: "%s", method: "%s", data: %s, dataType: "html"
                }).done(function(data) {
                  %s
                }).fail(function( jqXHR, textStatus ) {
                  %s
                });
           ''' % (url, method, data, success, fail)


class XsCallHtml(object):
  """
  Normal wrapper for an Ajax Call expecting to deal with HTML data (String, Dictionaries)
  This is the common way to query using Ajax. Data should be a python dictionary
  """
  url = 'reports/ajax'

  def __init__(self, pythonModule, ajaxMethod='POST'):
    """ Get the minimum information to create a Ajax request """
    if ajaxMethod not in ['POST', 'GET']:
      raise Exception('%s ajax method does not exist' % ajaxMethod)

    self.ajaxMethod = ajaxMethod
    self.pythonModule = pythonModule.replace(".py", "")

  def success(self, jsSucessFnc):
    """ Add the javascript method in case of success """
    self.jsSucessFnc = jsSucessFnc

  def ajax(self, data):
    """ Generic Ajax callback method """
    return '''
              $.ajax({
                    url: "../%s/%s", // 'http://192.168.9.30/test/suma.php',
                    method: "%s",
                    data: %s,
                    dataType: "html"
                }).done(function(data) {
                  %s
                }).fail(function( jqXHR, textStatus ) {
                  alert( "Request failed: " + textStatus );
                });
           ''' % (self.url, self.pythonModule, self.ajaxMethod, data, self.jsSucessFnc)

  def ajaxLocal(self, data):
    """ Generic Ajax callback method """
    return '''
              $.ajax({
                    url: "../%s/%s", // 'http://192.168.9.30/test/suma.php',
                    method: "%s",
                    data: %s,
                    dataType: "html"
                }).done(function(data) {
                    // Locally the request will never succeed
                }).fail(function( jqXHR, textStatus ) {

                  var rawFile = new XMLHttpRequest();
                  rawFile.open("GET", 'ajax_%s.json', false);
                  rawFile.onreadystatechange = function ()
                  {
                    if(rawFile.readyState === 4)
                    {
                      if(rawFile.status === 200 || rawFile.status == 0)
                      {
                        var allText = rawFile.responseText;
                        data = allText;
                      }
                    }
                  }
                  rawFile.send(null);
                  %s
                });
           ''' % (self.url, self.pythonModule, self.ajaxMethod, data, self.pythonModule, self.jsSucessFnc)


class XsCallFile(XsCallHtml):
  """
  Specific Ajax call to deal with files
  In this case Data are files object and it will pass this to the Python layer in order to perform some extra actions
  """
  url = None

  def ajax(self, data):
    """ Generic Ajax callback method """
    return '''
              $.ajax({
                    url: "../%s/%s", // 'http://192.168.9.30/test/suma.php',
                    method: "%s",
                    data: %s,
                    contentType: false,
                    cache: false,
                    processData: false,
                    async: false
                }).done(function(data) {
                  %s
                }).fail(function( jqXHR, textStatus ) {
                  alert( "Request failed: " + textStatus );
                });
           ''' % (self.url, self.pythonModule, self.ajaxMethod, data, self.jsSucessFnc)

  def ajaxLocal(self, data):
    """ Generic Ajax callback method """
    if self.url is None:
      raise Exception("URL has to be defined for this Ajax usage !!!")

    return '''
              $.ajax({
                    url: "../%s/%s", // 'http://192.168.9.30/test/suma.php',
                    method: "%s",
                    data: %s,
                    contentType: false,
                    cache: false,
                    processData: false,
                    async: false
                }).done(function(data) {
                    // Locally the request will never succeed
                }).fail(function( jqXHR, textStatus ) {

                  var rawFile = new XMLHttpRequest();
                  rawFile.open("GET", 'ajax_%s.json', false);
                  rawFile.onreadystatechange = function ()
                  {
                    if(rawFile.readyState === 4)
                    {
                      if(rawFile.status === 200 || rawFile.status == 0)
                      {
                        var allText = rawFile.responseText;
                        data = allText;
                      }
                    }
                  }
                  rawFile.send(null);
                  %s
                });
           ''' % (self.url, self.pythonModule, self.ajaxMethod, data, self.pythonModule, self.jsSucessFnc)
