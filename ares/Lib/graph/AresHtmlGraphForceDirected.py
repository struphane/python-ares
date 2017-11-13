""" Chart module in charge of generating a Forced directed Chart (network chart)
@author: Olivier Nogues

"""

import json
import re

from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg

regex = re.compile('[^a-zA-Z0-9_]')


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

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toNetwork(self.vals, self.chartKeys)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

  def setKeys(self, keys, selected=None):
    raise Exception("For Network chart please use the function - setGrpKeys")

  def setGrpKeys(self, grpKeys, selected=None):
    """ Set a default keys for the graph """
    self.chartKeys = [self.header[key] for key in grpKeys]
    self.selectedChartKey = "_".join(grpKeys[selected]) if selected is not None else "_".join(grpKeys[0])

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    if self.components:
      dataComp = "+ '_' + ".join([comp.val for comp in self.components])
      return "eval('%s_' + %s + '_' + %s)" % (self.htmlId, dataComp, self.dynKeySelection)

    return "eval('%s_' + %s )" % (self.htmlId, self.dynKeySelection)

  def jsUpdate(self):
    """ Add the Graph definition in the Javascript method """
    return '''
              d3.select("#%s svg").remove();
              d3.select("#%s").append("svg");
              var %s = nv.models.%s().%s ;
              %s
              d3.select("#%s svg").datum(%s).call(%s);
              nv.utils.windowResize(%s.update);
          ''' % (self.htmlId, self.htmlId, self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(), self.htmlId,
                   self.height, self.jqData, # recordSet key
                   self.getSvg(), self.htmlId, self.htmlId)

