"""

"""

from ares.Lib import AresHtml

class HandleRequest(AresHtml.Html):
  """

  """
  alias = "handleRequest"

  def __init__(self, aresObj, method, params, js="", cssCls=None, cssAttr=None):
    super(HandleRequest, self).__init__(aresObj, None, cssCls, cssAttr)
    self.method = method
    self.params = params
    self.js = js

  def onLoadFnc(self):
    return """$(document).ready(function() {
                $.post( '/reports/handlerequest/%s/%s?%s', function(result) { 
                            var res = JSON.parse(result) ;
                            var data = res.data ;
                            var status = res.status ;
                            if (status == 'Error') { 
                              alert(res.message) ; 
                              }
                            else {
                              %s ;
                              }
                                     });});""" % (self.method.__module__, self.method.__name__, ";".join(["%s=%s" % (k, v) for k, v in self.params.items()]), self.js)

  def __str__(self):
    return ""#'<div class="ares-loading"></div>'
