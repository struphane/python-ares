"""

"""

from Lib import AresChartsService
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlRadio


class NvD3Donut(AresHtmlContainer.Svg):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  alias, chartObject = 'donut', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html']
  __chartStyle = {'showLabels': 'true',
                  'labelThreshold': .05,
                  'labelType': '"percent"',
                  'donut': 'true',
                  'donutRatio': 0.35,
                  'x': "function(d) { return d[0]; }",
                  'y': "function(d) { return d[1]; }"}

  __svgProp = {
    'transition': '',
  }

  __chartProp = {
  #  'pie': {'startAngle': 'function(d) { return d.startAngle/2 -Math.PI/2 }',
  #          'endAngle': 'function(d) { return d.endAngle/2 -Math.PI/2 }'}
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def dataFnc(self, cat, val):
    """ Return the json data """
    return AresChartsService.toPie(self.vals, cat, val)

  def setKeys(self, keys, selected=None):
    """ Set a default key for the graph """
    if len(keys) == 1:
      self.selectedCat = keys[0]
      self.dfltCat =  keys[0]
      self.multiCat = False
    else:
      if selected is None:
        raise Exception("A selected category should be defined")

      self.selectedCat = selected
      self.multiCat = list(keys)
      self.dfltCat =  selected

  def setVals(self, vals, selected=None):
    """ Set a default value for the graph """
    if len(vals) == 1:
      self.selectedVal = vals[0]
      self.multiVal = False
      self.dfltVal = vals[0]
    else:
      if selected is None:
        raise Exception("A selected value should be defined")

      self.selectedVal = selected
      self.multiVal = list(vals)
      self.dfltVal = selected

  def jsUpdate(self):

    dispatchChart = []
    for displathKey, jsFnc in self.dispatch.items():
      dispatchChart.append("%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc))
    return '''
              var %s = nv.models.%s().%s ;

              %s

              d3.select("#%s svg").datum(%s)%s.call(%s);

              %s ;

              nv.utils.windowResize(%s.update);
            ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
                   self.htmlId, self.dataFnc(self.selectedCat, self.selectedVal), self.getSvg(), self.htmlId,
                   ";".join(dispatchChart), self.htmlId)

  def click(self, jsFnc):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = jsFnc

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      self.jsUpdate()
    )

  def selections(self):
    """ Return the possible data display option in the graph """
    categories, values = '', ''
    if self.multiCat:
      categories = AresHtmlRadio.Radio(self.aresObj, self.multiCat)
      categories.select(self.selectedCat)
      self.selectedCat = categories.val
      categories.click([self])
      #self.jsEvent['cat_%s' % self.htmlId] = categories.jsEvent['mouseup']

    if self.multiVal:
      values = AresHtmlRadio.Radio(self.aresObj, self.multiVal)
      values.select(self.selectedVal)
      self.selectedVal = values.val
      values.click([self])
      #self.jsEvent['val_%s' % self.htmlId] = values.jsEvent['mouseup']

    return "%s\n%s" % (categories, values)
