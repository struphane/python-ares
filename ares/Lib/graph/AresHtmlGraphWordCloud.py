""" Python Chart module to wrap the Work Cloud object
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg

class WordCloud(AresHtmlGraphSvg.Svg):
  """

  This module will require the javascript module: d3.layout.cloud.js

  TODO finalise the update method and make it generic with all the graph
  the update method should appear once and only once in the javascript section of the page
  """
  alias, reqJs = 'wordcloud', ['cloud']
  references = []
  width = 600

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toWordCloud(self.vals, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

  def jsUpdate(self):
    return '''
              d3.select("#%s svg g").remove();

              d3.layout.cloud().size([%s, %s])
              .words(%s) // Refer to the data variable
              .rotate(function() { return ~~(Math.random() * 2) * 90; })
              .font("Impact").fontSize(function(d) { return d.size; })
              .on("end", draw_new_%s).start();

              function draw_new_%s(words) {
                d3.select("#%s svg") // Refer to the chart variable
                  .append("g").attr("transform", "translate(150,150)").selectAll("text")
                  .data(words).enter().append("text").style("font-size", function(d) { return d.size + "px"; })
                  .style("font-family", "Impact").style("fill", function(d, i) {  return d3.scale.category20()(i); })
                  .attr("text-anchor", "middle")
                  .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
                  .text(function(d) {  return d.text; });
              } ;

              function drawCloudUpdate(words, jsGraphRef){
                 jsGraphRef
                    .selectAll("g").attr("transform", "translate(150,150)")
                    .selectAll("text").data(words).enter().append("text")
                      .style("font-size", function(d) { return d.size + "px"; }).style("font-family", "Impact")
                      .style("fill", function(d, i) { return fill(i); })
                      .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";  })
                      .text(function(d) { return d.text; });
              };
            ''' % (self.htmlId, self.width, self.height, self.jqData, self.htmlId, self.htmlId, self.htmlId)

