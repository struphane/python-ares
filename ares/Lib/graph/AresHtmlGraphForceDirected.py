"""

"""

#TODO test the new version of NVD3 sur github

from ares.Lib.html import AresHtmlContainer

class NvD3ForceDirected(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'forceDirected', 'forceDirectedGraph'
  references = ['http://nvd3.org/examples/lineWithFocus.html']
  __chartStyle = {
    'margin': '{top: 20, right: 20, bottom: 20, left: 20}',
    'color': 'function(d) { return d3Colors(d.group)',
    'nodeExtras': 'function(node) { node.append("text").attr("dx", 12).attr("dy", ".35em").text(function(d) { return d.name }); }'
    }

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        %s

        d3.select("#%s").datum(%s).call(%s);

      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.htmlId)
    )
