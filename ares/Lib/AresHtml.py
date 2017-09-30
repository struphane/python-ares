""" Main module for the HTML wrappers

The htmlId is generated by the report layer to ensure that there is no overlap between the ID
This will also help on having comprehensive ID

Please make sure that all the CSS information are defined in a CSS class

Aliases must be unique
"""

import os
import json
import collections
import warnings
import functools
import six

from ares.Lib import AresJs
from ares.Lib import AresItem


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('############################################################################')
        warnings.simplefilter('always', DeprecationWarning) #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) #reset filter
        warnings.simplefilter('############################################################################')
        return func(*args, **kwargs)
    return new_func


class Html(object):
  """
  Base class for any type of HTML object that the page can display

  THe logic of this module is quite simple.
  All the

  alias - Class variable just use to ensure function and HTML classes are correctly registered
  jsEvent -
  requirements -
  cssCls -

  Requirements
    - jquery-ui.js, for the nice display of the Tooltips, the Date picker and the Slider objects

  """
  alias, jsEvent, requirements = None, None, ['jquery-ui.js']
  cssCls, reference = None, None
  incIndent = 0
  reqJs, reqCss = None, None

  def __init__(self, aresObj, vals, cssCls=None):
    """ Create an python HTML object """
    self.aresObj = aresObj # The html object ID
    self.attr = {} if self.cssCls is None else {'class': self.cssCls} # default HTML attributes
    self.jsOnLoad, self.jsEvent, self.jsEventFnc = set(), {}, collections.defaultdict(set)
    self.vals = vals
    if cssCls is not None:
      self.attr['class'] = cssCls

    if self.aresObj is not None:
      # Some components are not using aresObj because they are directly used for the display
      if self.reqJs is not None:
        for js in self.reqJs:
          self.aresObj.jsImports.add(js)

      if self.reqCss is not None:
        for css in self.reqCss:
          self.aresObj.cssImport.add(css)

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  @property
  def jqId(self):
    """ Property to get the Jquery ID of a python HTML object """
    return '$("#%s")' % self.htmlId

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return '%s.val()' % self.jqId

  def addClass(self, cssCls, replace=False):
    """ Change the CSS Style of the HTML object """
    self.attr['class'] = cssCls if replace else "%s %s" % (self.attr['class'], cssCls)

  def toolTip(self, value):
    """ Add the Tooltip feature when the mouse is over the component """
    self.attr['title'] = value

  def attr(self, name, value):
    """ Set an attribute to the HTML object """
    self.attr[name] = value

  def strAttr(self):
    """ Return the string line with all the attributes """
    return 'id="%s" %s' % (self.htmlId, " ".join(['%s="%s"' % (key, val) for key, val in self.attr.items()]))

  def __str__(self):
    """ Return the String representation of an Python HTML object """
    raise NotImplementedError('subclasses must override __str__()!')

  def js(self, evenType, jsDef):
    """ Add a Javascript Event to an HTML object """
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, jsDef)

  def jsFromFile(self, evenType, fileName, variables=None):
    """ Add a Javascript even by loading a file """
    jsFile = open(os.path.join(self.aresObj.http["DIRECTORY"], 'js', fileName))
    jsDef = jsFile.read()
    if variables is not None:
      jsDef = jsDef % variables
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, jsDef)

  def update(self, data):
    """ Update the content of an HTML component """
    return '%s.html(%s);' % (self.jqId, data)

  def jsLinkTo(self, htmlObjs):
    """ Send the data to the different HTML objects in order to update them """
    for jqEven in self.jsEvent.values():
      for htmlObj in htmlObjs:
        jqEven.extendJsFnc(htmlObj.update(self.val))

  # ---------------------------------------------------------------------------------------------------------
  #                                          AJAX SECTION
  #
  # The below three methods are dedicated to interactively query the server. So there is not way to test it
  # fully locally. The only way to get it would be to upload the ajax scripts to the server and to test the
  # call from the local report
  #   - The GET method to pass variables in the URL
  #   - The POST method to pass variables in the call
  #   - The Json when the transfer is done using json type of data
  # ---------------------------------------------------------------------------------------------------------
  def get(self, evenType, url, data, jsDef, preAjaxJs=''):
    """
      Get method to get data directly by interacting with the page
      https://api.jquery.com/jquery.get/
    """
    data = 'eval(%s)' % data if isinstance(data, six.text_type) else json.dumps(data)
    jsDef = '%s $.get("%s", %s, function(data) { %s } );' % (preAjaxJs, url, data, jsDef)
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, jsDef, data=data, url=url)

  def post(self, evenType, url, data, jsDef, preAjaxJs='', redirectUrl=''):
    """
      Post method to get data directly by interacting with the page
      https://api.jquery.com/jquery.post/
    """
    data = '%s' % data if isinstance(data, (six.text_type, str)) else json.dumps(data)
    jsDef = '%s $.post("%s", %s, function(data) { %s } );' % (preAjaxJs, url, data, jsDef)
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, jsDef, data=data, url=url)

  def json(self, evenType, url, data, jsDef):
    """
      Special function to input Json data
      http://api.jquery.com/jquery.getjson/
    """
    data = 'eval(%s)' % data if isinstance(data, six.text_type) else json.dumps(data)
    jsDef = '$.getJSON("%s", %s, function(data) { %s });' % (url, data, jsDef)
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, jsDef, data=data, url=url)

  def onLoadFnc(self):
    """ Return a String with the Javascript method to put in the HTML report """
    return None

  def onLoad(self, loadFnc=None):
    """ Functions to get all the onload items for this object and all the underlying object """
    if loadFnc is None:
      loadFnc = self.jsOnLoad
    fnc = self.onLoadFnc()
    if fnc is not None:
      loadFnc.add(fnc)

    if isinstance(self.vals, list):
      for val in self.vals:
        if hasattr(val, 'onLoad'):
          getattr(val, 'onLoad')(loadFnc)
    else:
      if hasattr(self.vals, 'onLoad'):
        getattr(self.vals, 'onLoad')(loadFnc)
    return loadFnc

  def jsEvents(self, jsEventFnc=None):
    """ Function to get the Javascript methods for this object and all the underlying objects """
    if jsEventFnc is None:
      jsEventFnc = self.jsEventFnc
    for jEventType, jsEvent in self.jsEvent.items():
      jsEventFnc[jEventType].add(str(jsEvent))

    if isinstance(self.vals, list):
      for val in self.vals:
        if hasattr(val, 'jsEvent'):
          getattr(val, 'jsEvents')(jsEventFnc)
    else:
      if hasattr(self.vals, 'jsEvent'):
        getattr(self.vals, 'jsEvents')(jsEventFnc)
    return jsEventFnc

  def html(self):
    """ Return the onload, the HTML object and the javascript events """
    return self.onLoad(), str(self), self.jsEvents()

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj


class NavBar(object):
  """ """

  alias = None

  def __init__(self, titleAttr):
    """ """
    self.titleAttr = titleAttr

  def unstackTitles(self, titleLst):
    result = []
    result.append('<ul style="list-style-type:none">')
    for title in titleLst:
      result.append(r'<li><a href="#%s" class="w3-hover-green">%s</a></li>' % (title['value'], title['value']))
      if title['subObj']:
        result.append(self.unstackTitles(title['subObj']))
    result.append(r'</ul>')
    return '\n'.join(result)


  def html(self):
    """ """
    content = []
    if self.titleAttr['cssCls']:
      content.append('<div class="%s" style="width:%s%%">' % (self.titleAttr['cssCls'], self.titleAttr['width']))
    else:
      content.append('<div class="w3-sidebar w3-light-grey w3-bar-block" style="width:%s%%">' % self.titleAttr['width'])
    content.append(r'<h3 class="w3-bar-item">Navigation</h3>')
    content.append(self.unstackTitles(self.titleAttr['content']))
    content.append(r'</div>')
    return '\n'.join(content)
