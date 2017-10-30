""" Chart module in charge of generating a PlotBox Chart
@author: Olivier Nogues

"""
#TODO Migrate to the new Chart framework


from ares.Lib.html import AresHtmlContainer

class NvD3Sunburst(AresHtmlContainer.Svg):
  """ NVD3 Sunburst Chart python interface """
  alias, chartObject = 'sunburst', 'sunburstChart'
  references = ['http://bl.ocks.org/jensgrubert/7789216']
  __chartStyle = {
    'color': 'd3.scale.category20c()',
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        %s

        d3.select("#%s svg").datum(%s).call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.htmlId, self.htmlId)
    )