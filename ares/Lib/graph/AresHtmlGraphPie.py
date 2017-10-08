"""

"""

from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlRadio

class NvD3Pie(AresHtmlContainer.Svg):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  alias, chartObject = 'pie', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html']
  __chartStyle = {'showLabels': 'true',
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

  def dataFnc(self):
    """ Return the data Source converted to them be sent to the javascript layer """
    return "getDataFromRecordSet(%s, ['%s', '%s'])" % (self.jqRecordSet, self.selectedCat, self.selectedVal)

  def setKeys(self, keys, selected=None):
    """ Set a default key for the graph """
    if len(keys) == 1:
      self.selectedCat = keys[0]
      self.multiCat = False
    else:
      if selected is None:
        raise Exception("A selected category should be defined")

      self.selectedCat = selected
      self.multiCat = keys

  def setVals(self, vals, selected=None):
    """ Set a default value for the graph """
    if len(vals) == 1:
      self.selectedVal = vals[0]
      self.multiVal = False
    else:
      if selected is None:
        raise Exception("A selected value should be defined")

      self.selectedVal = selected
      self.multiVal = vals

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s().%s ;

        %s

        d3.select("#%s svg").datum(%s)%s.call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.getSvg(), self.htmlId, self.htmlId)
    )

  def selections(self):
    """ Return the possible data display option in the graph """
    categories, values = '', ''
    if self.multiCat:
      categories = AresHtmlRadio.Radio(self.aresObj, self.multiCat)
      categories.select(self.selectedCat)

    if self.multiVal:
      values = AresHtmlRadio.Radio(self.aresObj, self.multiVal)
      values.select(self.selectedVal)
    return "%s%s" % (categories, values)

  @property
  def jqCategory(self):
    """ Returns the selected category for the graph """
    return '$("#%s_col_selector option:selected")'% self.htmlId

  @property
  def jqValue(self):
    """ Return the selected value to use for the graph """
    return '$("#%s_val_selector option:selected")' % self.htmlId

  def jsUpdate(self):
    return ''