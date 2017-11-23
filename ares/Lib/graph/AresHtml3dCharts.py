""" Chart module in charge of generating a Spider Chart
@author: Olivier Nogues

"""
#TODO Add the legend

import json
# from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg
from ares.Lib.html import AresHtmlRadio
from ares.Lib.html import AresHtmlContainer
import re
regex = re.compile('[^a-zA-Z0-9_]')


class D3SpiderChart(AresHtmlGraphSvg.MultiSvg):
  """ NVD3 Spider Chart python interface """
  alias, chartObject = 'spider', 'multiBarChart'
  references = ['http://bl.ocks.org/nbremer/6506614',
                'http://bl.ocks.org/chrisrzhou/2421ac6541b68c1680f8']
  __chartStyle = {'w': '500', 'h': '600', 'levels': '10', 'maxValue': '10'}

  reqJs = ['vis']
  reqCss =  ['vis']
  series = None
  width = 300
  height = 250

  def __str__(self):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    return '''
              var colorscale = d3.scale.category10();
              var data = %s ;
              var LegendOptions = data.keys;
              var d = data.values ;

              var mycfg = {w: %s, h: %s, maxValue: 0.6, levels: 6, ExtraWidthX: 300};
              RadarChart.draw("#%s", d, mycfg);

              var svg = d3.select('#body').selectAll('svg').append('svg').attr("width", w+300).attr("height", h);
              var text = svg.append("text").attr("class", "title").attr('transform', 'translate(90,0)')
                            .attr("x", w - 70).attr("y", 10).attr("font-size", "12px").attr("fill", "#404040")
                            .text("What %% of owners use a specific service in a week");

              //Initiate Legend
              var legend = svg.append("g").attr("class", "legend").attr("height", 100)
                  .attr("width", 200).attr('transform', 'translate(90,20)');

              //Create colour squares
              legend.selectAll('rect').data(LegendOptions).enter().append("rect").attr("x", w - 65)
                .attr("y", function(d, i){ return i * 20;}).attr("width", 10).attr("height", 10)
                .style("fill", function(d, i){ return colorscale(i);});

              //Create text next to squares
              legend.selectAll('text').data(LegendOptions).enter().append("text").attr("x", w - 52)
                .attr("y", function(d, i){ return i * 20 + 9;}).attr("font-size", "11px")
                .attr("fill", "#737373").text(function(d) { return d; });

            ''' % (self.jqData, self.width, self.height-55, self.htmlId)

