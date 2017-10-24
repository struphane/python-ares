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

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var colorscale = d3.scale.category10();
        var LegendOptions = ['Smartphone','Tablet'];
        var d = %s ;

        var mycfg = {w: 500, h: 500, maxValue: 0.6, levels: 6, ExtraWidthX: 300};
        RadarChart.draw("#%s", d, mycfg);

        var svg = d3.select('#body').selectAll('svg').append('svg').attr("width", w+300).attr("height", h);
        var text = svg.append("text")
                      .attr("class", "title")
                      .attr('transform', 'translate(90,0)')
                      .attr("x", w - 70)
                      .attr("y", 10)
                      .attr("font-size", "12px")
                      .attr("fill", "#404040")
                      .text("What %% of owners use a specific service in a week");

        //Initiate Legend
        var legend = svg.append("g")
          .attr("class", "legend")
          .attr("height", 100)
          .attr("width", 200)
          .attr('transform', 'translate(90,20)');

          //Create colour squares
          legend.selectAll('rect')
            .data(LegendOptions)
            .enter()
            .append("rect")
            .attr("x", w - 65)
            .attr("y", function(d, i){ return i * 20;})
            .attr("width", 10)
            .attr("height", 10)
            .style("fill", function(d, i){ return colorscale(i);});
          //Create text next to squares
          legend.selectAll('text')
            .data(LegendOptions)
            .enter()
            .append("text")
            .attr("x", w - 52)
            .attr("y", function(d, i){ return i * 20 + 9;})
            .attr("font-size", "11px")
            .attr("fill", "#737373")
            .text(function(d) { return d; })
            ;
      ''' % (self.dataFnc(), self.htmlId)
    )

  def __str__(self):
    """ Return the svg container """
    return '<div id="body"><div %s></div></div>' % self.strAttr()