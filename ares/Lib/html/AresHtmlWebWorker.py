"""

"""

from ares.Lib import AresHtml
from flask import render_template_string


class WebWorker(AresHtml.Html):
  """ This module should create web workers for any javascript functions
  """
  references = ['https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers',
                'https://www.synbioz.com/blog/introduction_aux_web_workers']
  alias, cssCls = 'worker', ['btn', 'btn-success']
  __reqCss = ['bootstrap', 'jquery']
  __reqJs = ['worker'] # this will force the worker refresh on the client side

  @AresHtml.inprogress
  def __init__(self, aresObj, htmlObj, jsFile):
    """ Define the script attached to the worker in the main module """
    self.aresObj = aresObj
    for css in self.__reqCss:
      self.aresObj.cssImport.add(css)
    for js in self.__reqJs:
      self.aresObj.jsImports.add(js)
    self.attr = {'class': set([])} if self.cssCls is None else {'class': set(self.cssCls)} # default HTML attributes
    self.htmlObj = htmlObj # the Html object updated during the worker run
    self.jsFile = jsFile # The javascript file with the worker code
    self.aresObj.jsGlobal.add("%s" % self.htmlId)
    if not self.htmlId in self.aresObj.workers:
      self.aresObj.workers[self.htmlId] = self

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  def onmessage(self, jsFragment):
    """ Define the javascript event for the worker """
    return '''
             %s.onmessage  = function(e) {
                  %s ;
              }
           ''' % (self.htmlId, jsFragment)

  def terminate(self):
    """ Stop the worker to run """
    return "%s.terminate() ;" % self.htmlId

  def stop(self):
    """ Returns the javascript function to stop the worker """
    return "%s.close() ;" % self.htmlId

  def __str__(self):
    """ Display a button to start the worker process """
    workerJsUrl = render_template_string("{{ url_for('static',filename='js/%s') }}" % self.jsFile)
    self.aresObj.jsOnLoadFnc.add('''
          $('#button_%s').on("click", function (e){
              var w = %s;  
              if(typeof(Worker) !== "undefined") {
                  if(typeof(w) == "undefined") {w = new Worker("%s");}
                  w.postMessage("youpi");
                  w.onmessage = function(event) { 
                    display(event.data); 
                  };
                  
              } else { display("Sorry! No Web Worker support."); }
          }) ''' % (self.htmlId, self.htmlId, workerJsUrl))
    return "<button id='button_%s' %s>Start Worker</button>" % (self.htmlId, self.strAttr(False))

  def onLoad(self, loadFnc=None):
    return {}

  def jsEvents(self, jsEventFnc=None):
    return {}