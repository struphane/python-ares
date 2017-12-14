""" Python Chart module to wrap the Work Cloud object
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class XWordCloud(AresHtmlGraphSvg.XSvg):
  """ NVD3 Word Cloud Chart python interface """
  alias, reqJs = 'wordcloud', ['cloud']
  references = ['https://www.jasondavies.com/wordcloud/']
  width = 600
  factor = 1

  def scaling(self, factor):
    """ Rescale the values to have fit the page

    :param factor: The scaling factor > 1
    :return:
    """
    self.factor = factor

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    return '''
              %(chartDimension)s ;
              d3.select("#%(htmlId)s svg g").remove();

              d3.layout.cloud().size([%(width)s, %(height)s])
              .words(%(data)s) // Refer to the data variable
              .rotate(function() { return ~~(Math.random() * 2) * 90; })
              .font("Impact").fontSize(function(d) { return d.value / %(factor)s; })
              .on("end", draw_new_%(htmlId)s).start();

              function draw_new_%(htmlId)s(words) {
                d3.select("#%(htmlId)s svg") // Refer to the chart variable
                  .append("g").attr("transform", "translate(150,150)").selectAll("text")
                  .data(words).enter().append("text").style("font-size", function(d) { return d.size + "px"; })
                  .style("font-family", "Impact").style("fill", function(d, i) {  return %(color)s[i]; })
                  .attr("text-anchor", "middle")
                  .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
                  .text(function(d) { return d.text; });
              } ;

              function drawCloudUpdate(words, jsGraphRef){
                 jsGraphRef
                    .selectAll("g").attr("transform", "translate(150,150)")
                    .selectAll("text").data(words).enter().append("text")
                      .style("font-size", function(d) { return d.value + "px"; }).style("font-family", "Impact")
                      .style("fill", function(d, i) { return fill(i); })
                      .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";  })
                      .text(function(d) { return d.key; });
              };
            ''' % {'htmlId': self.htmlId, 'width': self.width, 'height': self.height, 'data': data['data'], 'chartDimension': data['vars'],
                   'factor': self.factor, 'color': json.dumps(AresHtmlGraphSvg.XSvg.colorCharts)}

