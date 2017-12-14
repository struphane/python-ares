""" Module dedicated to register the data on the javascript part but also to display fiilters on the HTML layers to interact with it.
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
    self.xFilter = filter
    if val is not None:
      self.htmlId = "%s_%s_%s" % (filter.htmlId, key, val)
    else:
      # This dimension is never used in the process to aggregate results
      # It is an internal dimension to be able to filter on the recordSet
      self.htmlId = "%s_%s" % (filter.htmlId, key)
    self.jsVar = {'htmlId': self.htmlId, 'val': val, 'key': key, 'filterId': filter.htmlId}

  def filter(self, col, htmlObj, val=None):
    """

    .filter( function (d) { var val = %s; if (val == 'all') {return true} else {return d.key == val }; } )
    :return:
    """
    if col != self.jsVar['key'] :
      raise Exception("%s column different from the one defined in the CrossFilter dimension %s" % (col, self.key))

    self.filters.add(htmlObj)
    if val is not None:
      self.jsVar['filterVal'] = "'%s'" % val
      self.jsVar['filter'] = ".filter( function (d) { var val = '%s'; if (val == 'all') { return true } else { return d == val } } )" % val
    else:
      self.jsVar['filterVal'] = htmlObj.val
      self.jsVar['filter'] = ".filter( function (d) { var val = %s; if (val == 'all') { return true } else { return d == val } } )" % htmlObj.val

    self.aresObj.jsGlobal.add("%(htmlId)s_dim = %(filterId)s.dimension(function(d) {  return d['%(key)s'] ; } ) " % self.jsVar)
    self.jsVar['filterDef'] = "%(htmlId)s_dim%(filter)s" % self.jsVar

  def removeFilters(self):
    """ remove all the filters already attached to this crossfilter object and dimension

    :return: A string corresponding to the javascript function to remove crossfilter filters
    """
    return "%(htmlId)s_dim.filterAll()" % self.jsVar

  def dimension(self):
    """ Return the result of a dimension

    :return:
    """
    if 'filter' not in self.jsVar:
      self.aresObj.jsGlobal.add("%(htmlId)s_dim = %(filterId)s.dimension(function(d) {  return d['%(key)s'] ; } )" % self.jsVar)

    return "%(htmlId)s_dim.group().reduceSum( function(d) { return +d['%(val)s'] ; } )" % self.jsVar

  def val(self):
    """

    :return:
    """
    return "%(htmlId)s_dim.top(Infinity)" %  self.jsVar

  def data(self):
    """

    :return:
    """
    self.jsVar['vars'] = []
    for col, filterGrp in self.xFilter.filters.items():
      filter = filterGrp[1]
      if col != self.jsVar['key']:
        self.jsVar['vars'].append(filter.removeFilters())
        self.jsVar['vars'].append("var x%(htmlId)s_data = %(filterDef)s.group().reduceSum( function(d) { return +d['%(val)s'] ; } ).top(Infinity)" % filter.jsVar)
        self.jsVar['vars'].append("xData = []")
        self.jsVar['vars'].append("x%(htmlId)s_data.forEach( function(p, i) { if ( (p.key == %(filterVal)s) || (%(filterVal)s == 'all') ) {xData.push(p)} else { xData.push( {key: p.key, value: 0 }) ; } } )" % filter.jsVar)
    if 'filter' in self.jsVar:
      self.jsVar['vars'].append(self.removeFilters())
      self.jsVar['vars'].append("var x%(htmlId)s_data = %(filterDef)s.group().reduceSum( function(d) { return +d['%(val)s'] ; } ).top(Infinity) ;" % self.jsVar)
      self.jsVar['vars'].append("xData = []")
      self.jsVar['vars'].append("x%(htmlId)s_data.forEach( function(p, i) { if ( (p.key == %(filterVal)s) || (%(filterVal)s == 'all') ) {xData.push(p)} else { xData.push( {key: p.key, value: 0 }) ; } } );" % self.jsVar)
      return {'vars': ";".join(self.jsVar['vars']), 'data': 'xData'}

    return {'vars': ";".join(self.jsVar['vars']), 'data': "%s.top(Infinity)" % self.dimension()}


class HtmlDataCrossFilter(object):
  """ Special object to manage recordSet """
  reqJs = ['crossfilter']
  references = ['http://dc-js.github.io/dc.js/examples/download-table.html',
                'https://stackoverflow.com/questions/33102032/crossfilter-group-a-filtered-dimension']

  def __init__(self, aresObj, recordSet, header):
    """ Instantiate the Cross Filter object

    :param aresObj: The ares Object
    :param recordSet: The recordSet with all your data to be used
    :param header: The recordSet header definition
    :return:
    """
    self.aresObj = aresObj # The html object ID
    for js in self.reqJs:
      self.aresObj.jsImports.add(js)
    self.recordSet, self.header = recordSet, header # Store the recordSet information
    self.links, self.filters, self.grps, self.charts = set(), {}, {}, set()
    self.aresObj.jsGlobal.add(" %s = crossfilter(%s)" % (self.htmlId, json.dumps(self.recordSet)))

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  def group(self, colGrp, valGrp):
    """ CrossFilter grouping function

    :param colGrp: The key in the recordset used as key to aggregate the data
    :param valGrp: The key in the recordset used as val to aggregate the data
    :return:
    """
    groupOjb = CrossFilterGroup(self.aresObj, self, colGrp, valGrp)
    self.grps[colGrp] = groupOjb # Store the different group attached to a crossFilter python wrapper object
    return groupOjb

  def addFilter(self, col, title, cssCls=None, cssAttr=None):
    """ Add a CrossFilter filter to the recordset. The process will find out the correct dimension on which this filter
    should be applied

    :param col: The column used as a filter.
    :param title: The title of the filter
    :param cssCls: The class for the selection HTML component
    :param cssAttr: The CSS attribute
    :return:
    """
    filVals = sorted(list(set([rec[col] for rec in self.recordSet])))
    if len(filVals) > 20:
      # Change automatically the component to a input text box with selection
      filerObj = self.aresObj.input(title, dflt='all', cssCls=cssCls, cssAttr=cssAttr)
      filerObj.autocomplete(['all'] + filVals)
    else:
      filerObj = self.aresObj.select(['all'] + filVals, title, cssCls=cssCls, cssAttr=cssAttr)
    if not col in self.grps:
      # The process will automatically construct the missing dimension
      self.group(col, 'tip')
    self.grps[col].filter(col, filerObj)
    self.filters[col] = (filerObj, self.grps[col])
    return filerObj

  def addTextFilter(self, col, title, cssCls=None, cssAttr=None):
    """

    :param col:
    :param title:
    :param cssCls:
    :param cssAttr:
    :return:
    """
    filVals = sorted(list(set([rec[col] for rec in self.recordSet])))
    filerObj = self.aresObj.input(title, dflt='all', cssCls=cssCls, cssAttr=cssAttr)
    if not col in self.grps:
      # The process will automatically construct the missing dimension
      self.group(col, 'tip')
    self.grps[col].filter(col, filerObj)
    self.filters[col] = (filerObj, self.grps[col])
    return filerObj

  def display(self, dimension):
    """ Debug function to be able to see easily the result of your CrossFilter implementation for a specified dimension

    :param dimension: The python dimension object
    :return:
    """
    self.aresObj.jsOnLoadFnc.add('''var $input = $("<input type='button' id='%s_button' value='new button' />"); $input.appendTo($('#page-content-wrapper'));''' % self.htmlId)
    self.aresObj.jsOnLoadFnc.add(''' $('#%s_button').on('click',function(){ %s; alert(%s.toSource()) ; }); ''' % (self.htmlId, dimension.data()['vars'], dimension.data()['data']))

