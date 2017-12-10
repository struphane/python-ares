""" Module dedicated to register the data on the javascript part but also to display fiilters on the HTML layers to
interact with it.
@author: Olivier Nogues

"""

import json
import collections

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


class CrossFilterGroup(object):
  """

  """

  def __init__(self, aresObj, filter, key, val):
    """

    :return:
    """
    self.aresObj = aresObj
    self.links, self.filters = set(), set()
    self.filterId = filter.htmlId
    self.htmlId = "%s_%s_%s" % (filter.htmlId, key, val)
    self.jsVar = {'htmlId': self.htmlId, 'val': val, 'key': key, 'filterId': filter.htmlId}
    self.aresObj.jsGlobal.add(" %(htmlId)s_dim = %(filterId)s.dimension( function(d) {return d['%(key)s'] ;} )" % self.jsVar)
    self.aresObj.jsGlobal.add(" %(htmlId)s = %(htmlId)s_dim.group().reduceSum( function(d) { return +d['%(val)s'] ; } )" % self.jsVar)

  def filter(self, htmlObj):
    """

    .filter( function (d) { var val = %s; if (val == 'all') {return true} else {return d.key == val }; } )
    :return:
    """
    self.filters.add(htmlObj)


  def data(self):
    """

    :return:
    """
    data = ["%s.top(Infinity)" % self.htmlId]
    for filter in self.filters:
      data.append("filter( function (d) { var val = %s; if (val == 'all') {return true} else {return d.key == val }; } )" % filter.val)
    return ".".join(data)


class HtmlDataCrossFilter(object):
  """ Special object to manage recordSet """
  reqJs = ['crossfilter']
  references = ['http://dc-js.github.io/dc.js/examples/download-table.html']

  def __init__(self, aresObj, data, header):
    """ Transform data from Python to Javascript """
    self.aresObj = aresObj # The html object ID
    for js in self.reqJs:
      self.aresObj.jsImports.add(js)
    self.recordSet = data
    self.links, self.filters, self.grps = set(), set(), collections.defaultdict(list)
    self.aresObj.jsGlobal.add(" %s = crossfilter(%s)" % (self.htmlId, json.dumps(self.recordSet)))

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  def group(self, key, val):
    """
    :param key:
    :param val:
    :return:
    """
    groupOjb = CrossFilterGroup(self.aresObj, self, key, val)
    self.grps[key].append(groupOjb)
    return groupOjb

  def addFilter(self, col, cssCls=None, cssAttr=None):
    """ Add a filter to the dictionary """
    filVals = sorted(list(set([rec[col] for rec in self.recordSet])))
    filerObj = self.aresObj.select(['all'] + filVals, 'Youpi', cssCls=cssCls, cssAttr=cssAttr)
    for grp in self.grps[col]:
      grp.filter(filerObj)
    self.filters.add(filerObj)
    return filerObj

  def get(self, val):
    """ Return the value of a javascript dictionary """
    return "%s[%s]" % (self.htmlId, val)


