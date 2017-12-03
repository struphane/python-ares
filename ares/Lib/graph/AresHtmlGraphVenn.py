""" Chart module in charge of generating a Venn Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlRadio
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlGraphSvg


class NvD3Venn(AresHtmlGraphSvg.Svg):
  """ NVD3 Venn Chart python interface """
  alias, chartObject = 'venn', 'pieChart'
  references = ['https://github.com/benfred/venn.js',
                'http://bl.ocks.org/bessiec/986e971203b4b8ddc56d3d165599f9d0']
  __chartStyle = {'width': 500, 'height': 200}

  __svgProp = {
  }

  __chartProp = {
  }
  height = 200

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['venn']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toVenn(self.vals, self.chartKeys[0], self.chartKeys[1], self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def setKeys(self, keys, selected=None):
    """ Set a default key for the graph """
    if not isinstance(keys, list) or len(keys) != 2:
      raise Exception("You should supply two columns for this type of charts")

    self.chartKeys = keys
    self.selectedChartKey = "_".join(keys)

  def setVals(self, vals, selected=None):
    """ Set a default value for the graph """
    self.chartVals = [self.header[val] for val in vals]
    self.selectedChartVal = vals[selected] if selected is not None else vals[0]

  def __str__(self):
    """ Return the svg container """
    self.processData()
    categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys], cssAttr={'display': 'None'}, internalRef='key_%s' % self.htmlId)
    categories.select(self.selectedChartKey)
    self.dynKeySelection = categories.val # The javascript representation of the radio
    values = AresHtmlRadio.Radio(self.aresObj, [val for val, _, _ in self.chartVals], cssAttr={'display': 'None'}, internalRef='val_%s' % self.htmlId)
    values.select(self.selectedChartVal)
    self.dynValSelection = values.val # The javascript representation of the radio

    categories.click([self])
    values.click([self])

    self.htmlContent.append(str(categories))
    self.htmlContent.append(str(values))
    self.htmlContent.append('<div %s></div>' % self.strAttr())
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)

  def jsUpdate(self):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    return '''
              var chartId = '%s' ;
              var %s = venn.VennDiagram().%s ;
              %s
              d3.select("#" + chartId).style("height", '%spx').datum(%s)%s.call(%s);
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

              var div = d3.select("#" + chartId);
              div.selectAll("g")
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
            ''' % (self.htmlId, self.htmlId, self.attrToStr(), self.propToStr(),
                   self.height, self.jqData, # recordSet key
                   self.getSvg(), self.htmlId, self.htmlId)


