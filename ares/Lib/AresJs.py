""" Python Wrapper for Pure javascript call

This will be the helper for the Ajax calls

This module require jQuery
reference website: http://api.jquery.com/jquery.ajax/

"""

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
