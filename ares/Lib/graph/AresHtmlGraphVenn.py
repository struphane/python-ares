""" Chart module in charge of generating a Pie Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg
import re

regex = re.compile('[^a-zA-Z0-9_]')

class NvD3Venn(AresHtmlGraphSvg.Svg):
  """ NVD3 Pie Chart python interface """
  alias, chartObject = 'venn', 'pieChart'
  references = ['https://github.com/benfred/venn.js']
  __chartStyle = {}

  __svgProp = {
    #'transition': '',
  }

  __chartProp = {
  #  'pie': {'startAngle': 'function(d) { return d.startAngle/2 -Math.PI/2 }',
  #          'endAngle': 'function(d) { return d.endAngle/2 -Math.PI/2 }'}
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['venn']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toPie(self.vals, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = [ {sets: ['A'], size: 12},{sets: ['B'], size: 12}, {sets: ['A','B'], size: 2}]; ;" % (self.htmlId, regex.sub('', key.strip()), json.dumps(vals)))

  def jsUpdate(self):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    return '''
              var chartId = '%s' ;
              d3.select("#"+ chartId +" svg").remove();
              var %s = venn.VennDiagram() ;
              %s
              d3.select("#" + chartId).style("height", '%spx').datum(eval(%s))%s.call(%s);
              nv.utils.windowResize(%s.update);

              var tooltip = d3.select("body").append("div").attr("class", "venntooltip");

              d3.selectAll("#" + chartId + " .venn-circle")
                .on("mouseover", function(d, i) {
                    var node = d3.select(this).transition();
                    node.select("path").style("fill-opacity", .2);
                    node.select("text").style("font-weight", "100")
                                       .style("font-size", "36px");

                })
                .on("mouseout", function(d, i) {
                    var node = d3.select(this).transition();
                    node.select("path").style("fill-opacity", 0);
                    node.select("text").style("font-weight", "100")
                                       .style("font-size", "24px");
                });

              d3.select("#" + chartId).selectAll("g")
                  .on("mouseover", function(d, i) {
                      // sort all the areas relative to the current item
                      venn.sortAreas(div, d);

                      // Display a tooltip with the current size
                      tooltip.transition().duration(400).style("opacity", .9);
                      tooltip.text(d.size + " users");

                      // highlight the current path
                      var selection = d3.select(this).transition("tooltip").duration(400);
                      selection.select("path")
                          .style("fill-opacity", d.sets.length == 1 ? .4 : .1)
                          .style("stroke-opacity", 1);
                  })

                  .on("mousemove", function() {
                      tooltip.style("left", (d3.event.pageX) + "px")
                             .style("top", (d3.event.pageY - 28) + "px");
                  })

                  .on("mouseout", function(d, i) {
                      tooltip.transition().duration(400).style("opacity", 0);
                      var selection = d3.select(this).transition("tooltip").duration(400);
                      selection.select("path")
                          .style("fill-opacity", d.sets.length == 1 ? .25 : .0)
                          .style("stroke-opacity", 0);
                  });
            ''' % (self.htmlId, self.htmlId, self.propToStr(),
                   self.height, self.jqData, # recordSet key
                   self.getSvg(), self.htmlId, self.htmlId)


