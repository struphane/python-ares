""" Module dedicated to register the data on the javascript part but also to display fiilters on the HTML layers to
interact with it.
@author: Olivier Nogues

"""

import json

from ares.Lib import AresHtml
from ares.Lib.html import AresHtmlInput


class HtmlData(AresHtml.Html):
  """ Base class to store the data """

  def __init__(self, aresObj, data):
    """ Transform data from Python to Javascript """
    super(HtmlData, self).__init__(aresObj, data)

  def __store(self, globalVar=True):
    """ Store the variable as a javascript variable """
    if globalVar:
      self.aresObj.jsGlobal.add(" %s = %s " % (self.htmlId, json.dumps(self.vals)))

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  @property
  def jqId(self):
    """ """
    return self.htmlId

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return self.jqId

  def __str__(self):
    """ """
    self.__store()
    return ''


class HtmlDataDic(HtmlData):
  """ Special object to manage recordSet """

  def addFilter(self, key, value, label, cssCls=None, cssAttr=None):
    """ Add a filter to the dictionary """
    AresHtmlInput.InputText(self.aresObj, value, cssCls=cssCls, cssAttr=cssAttr, htmllId="filter_%s_%s" % (self.htmlId, key))

  def get(self, val):
    """ Return the value of a javascript dictionary """
    return "%s[%s]" % (self.htmlId, val)


class HtmlDataRec(HtmlData):
  """ Special object to manage recordSet """

  def addFilter(self, key, value, label, cssCls=None, cssAttr=None):
    """ Add a filter to the dictionary """
    AresHtmlInput.InputText(self.aresObj, value, cssCls=cssCls, cssAttr=cssAttr, htmllId="filter_%s_%s" % (self.htmlId, key))

  def get(self, val):
    """ Return the value of a javascript dictionary """
    return "%s[%s]" % (self.htmlId, val)
