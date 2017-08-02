""" Python Wrapper for Pure javascript call

This will be the helper for the Ajax calls

This module require jQuery
reference website: http://api.jquery.com/jquery.ajax/
"""

class XsCall(object):
  """

  data should be a python dictionary
  """

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
                    url: "../reports_ajax/%s", // 'http://192.168.9.30/test/suma.php',
                    method: "%s",
                    data: %s,
                    dataType: "html"
                }).done(function(data) {
                  %s
                }).fail(function( jqXHR, textStatus ) {
                  alert( "Request failed: " + textStatus );
                });
           ''' % (self.pythonModule, self.ajaxMethod, data, self.jsSucessFnc)

  def ajaxLocal(self, data):
    """ Generic Ajax callback method """
    return '''
              $.ajax({
                    url: "../reports_ajax/%s", // 'http://192.168.9.30/test/suma.php',
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
           ''' % (self.pythonModule, self.ajaxMethod, data, self.pythonModule, self.jsSucessFnc)