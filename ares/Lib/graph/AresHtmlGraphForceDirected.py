""" Chart module in charge of generating a Forced directed Chart (network chart)
@author: Olivier Nogues

"""

import json

from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlRadio


class NvD3ForceDirected(AresHtmlGraphSvg.Svg):
  """ """
  alias, chartObject = 'forceDirected', 'forceDirectedGraph'
  references = ['http://krispo.github.io/angular-nvd3/#/forceDirectedGraph']
  __chartStyle = {
    'width ': '500',
    'height': '400',
    'margin': '{top: 20, right: 20, bottom: 20, left: 20}',
    'color': 'function(d) { return d3.scale.category20()(d.group)}',
    'nodeExtras': 'function(node) { node.append("text").attr("dx", 12).attr("dy", ".35em").text(function(d) { return d.name }); }'
    }

  __chartProp = {
    'dispatch': {'on': "'renderEnd', function(){console.log('render complete');}"}
  }

  # Required CSS and JS modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toNetwork(self.vals, self.chartKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def processDataMock(self, cat=None, val=None):
    """ Return the json data """
    self.chartKeys = [('MOCK', None, None)]
    self.selectedChartKey = 'MOCK'
    self.aresObj.jsGlobal.add("data_%s = {'%s': %s}" % (self.htmlId, self.selectedChartKey, open(r"ares\json\%sData.json" % self.alias).read().strip()))

  def setKeys(self, keys, selected=None):
    raise Exception("For Network chart please use the function - setGrpKeys")

  def setGrpKeys(self, grpKeys, selected=None):
    """ Set a default keys for the graph """
    self.chartKeys = grpKeys
    self.selectedChartKey = "_".join(grpKeys[selected]) if selected is not None else "_".join(grpKeys[0])

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    if self.components:
      dataComp = "+ '_' + ".join([comp.val for comp in self.components])
      return "data_%s[%s + '_' + %s]" % (self.htmlId, dataComp, self.categories.val)

    return "data_%s[%s]" % (self.htmlId, self.categories.val)

  def jsUpdate(self, data=None):
    """ Add the Graph definition in the Javascript method """
    data = data if data is not None else self.jqData
    return '''
              d3.select("#%(htmlId)s svg").remove();
              d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s)%(svgProp)s.call(%(htmlId)s);
              nv.utils.windowResize(%(htmlId)s.update);
          ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                 'chartProp': self.propToStr(), 'height': self.height, 'data': data, 'svgProp': self.getSvg()}

  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {},
                                          internalRef='key_%s' % self.htmlId, checked=self.selectedChartKey)
    self.categories.click([self])

    self.htmlContent.append(str(self.categories))
    self.htmlContent.append('<div %s><svg style="width:100%%;height:%spx;"></svg></div>' % (self.strAttr(), self.height))
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)