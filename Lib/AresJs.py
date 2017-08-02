""" Python Wrapper for Pure javascript call

This will be the helper for the Ajax calls

This module require jQuery
reference website: http://api.jquery.com/jquery.ajax/
"""

import Lib.AresHtml as AresHtml

class XsCall(object):
  """

  data should be a python dictionary
  """

  def __init__(self, alias, pythonModule, jsSucessFnc, ajaxMethod='POST'):
    """ Get the minimum information to create a Ajax request """
    self.alias = alias
    if ajaxMethod not in ['POST', 'GET']:
      raise Exception('%s ajax method does not exist' % ajaxMethod)

    self.jsSucessFnc = jsSucessFnc
    self.ajaxMethod = ajaxMethod
    self.pythonModule = pythonModule.replace(".py", "")

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

class XSSave(AresHtml.Button):
  """

  """

  def ajax(self):
    """

    """

class XSValidate(AresHtml.Button):
  """

  """

  def ajax(self):
    """

    """

class XSComments(AresHtml.Button):
  """

  """

  def ajax(self):
    """

    """