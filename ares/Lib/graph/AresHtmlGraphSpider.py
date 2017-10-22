"""

"""

from ares.Lib.html import AresHtmlContainer

class D3SpiderChart(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'spider', 'multiBarChart'
  references = ['http://nvd3.org/examples/multiBar.html']
  __chartStyle = {'w': '500',
                  'h': '600',
                  'levels': '10',
                  'maxValue': '10'
                  }

  reqJs = ['spider']
  series = None

  def dataFnc(self):
    """ Add the data function to transform the python data structure into the one expected by the spider chart"""

  def selectSeries(self):
    """ """
    for headerLine in self.header:
      if headerLine.get('type') == 'series':
        self.series = headerLine.get('values', [])


  # def graph(self):
  #   """ Add the Graph definition in the Javascript method """
  #   chartCfg = "%s" % ','.join(['%s: %s' % (key, val) for key, val in __chartStyle.items()])
  #   self.selectSeries()
  #   self.aresObj.jsGraphs.append(
  #     '''
  #       var cfg = { %s }
  #     
  #       var colorscale = d3.scale.category10();
  #       
  #       var legendOptions = [];
  #       //extract Selected Series
  #       
  #       var selectedSeries = %s;
  #       
  #       selectedSeries.each(function () {
  #       legendOptions.push($(this).val());
  #       })
  #       
  #       var data = getSpiderRecSet(%s, %s, selectedSeries);
  #       
  #       RadarChart.draw("#%s", data, cfg);
  #       
  #       var svg = d3.select('#%s svg')
  #           .selectAll('svg')
  #           .append('svg')
  #           .attr("width", %s+300)
  #           .attr("height", %s)
  #       
  #       var legend = svg.append("g")
  #             .attr("class", "legend")
  #             .attr("height", 100)
  #             .attr("width", 200)
  #             .attr('transform', 'translate(90,20)') 
  #             ;
  #                     
  #       //Create colour squares
  #       legend.selectAll('rect')
  #         .data(LegendOptions)
  #         .enter()
  #         .append("rect")
  #         .attr("x", %s - 65)
  #         .attr("y", function(d, i){ return i * 20;})
  #         .attr("width", 10)
  #         .attr("height", 10)
  #         .style("fill", function(d, i){ return colorscale(i);})
  #         ;
  #       
  #       //Create text next to squares
  #       legend.selectAll('text')
  #         .data(LegendOptions)
  #         .enter()
  #         .append("text")
  #         .attr("x", %s - 52)
  #         .attr("y", function(d, i){ return i * 20 + 9;})
  #         .attr("font-size", "11px")
  #         .attr("fill", "#737373")
  #         .text(function(d) { return d; })
  #         ;	
  #       
  #     ''' % (chartCfg, self.jqSeries, self.jqRecordSet, self.jqC, self.htmlId, self.htmlId,
  #            self.__chartStyle['w'], self.__chartStyle['h'], self.__chartStyle['w'], self.__chartStyle['w'])
  #   )