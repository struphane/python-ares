""" Chart module in charge of generating a Spider Chart
@author: Olivier Nogues

"""
#TODO Add the legend

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti
from ares.Lib.html import AresHtmlRadio
from ares.Lib.html import AresHtmlContainer


class D3SpiderChart(AresHtmlGraphSvgMulti.MultiSvg):
  """ NVD3 Spider Chart python interface """
  alias, chartObject = 'spider', 'multiBarChart'
  references = ['http://bl.ocks.org/nbremer/6506614',
                'http://bl.ocks.org/chrisrzhou/2421ac6541b68c1680f8']
  __chartStyle = {'w': '500', 'h': '600', 'levels': '10', 'maxValue': '10'}

  reqJs = ['spider']
  series = None
  width = 300
  height = 250

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toSpider(self.vals, self.chartKeys, self.selectedX , self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
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

            ''' % (data, self.width, self.height-55, self.htmlId)

  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys],
                                          cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {}, checked=self.selectedChartKey)
    self.values = AresHtmlRadio.Radio(self.aresObj, [val for val, _, _ in self.chartVals],
                                      cssAttr={'display': 'None'} if len(self.chartVals) == 1 else {}, checked=self.selectedChartVal)

    self.categories.click([self])
    self.values.click([self])

    self.htmlContent.append(str(self.categories))
    self.htmlContent.append(str(self.values))
    self.htmlContent.append('<div id="body"><div %s></div></div>' % self.strAttr())
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)