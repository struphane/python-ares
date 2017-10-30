""" Chart module in charge of generating a Forced directed Chart (network chart)
@author: Olivier Nogues

"""
#TODO Migrate to the new Chart framework

from ares.Lib.html import AresHtmlContainer

class NvD3ForceDirected(AresHtmlContainer.Svg):
  """ """
  alias, chartObject = 'forceDirected', 'forceDirectedGraph'
  references = ['http://krispo.github.io/angular-nvd3/#/forceDirectedGraph']
  __chartStyle = {
    'width ': '500',
    'height': '400',
    'margin': '{top: 20, right: 20, bottom: 20, left: 20}',
    'color': 'function(d) { return d3.scale.category20()(d.group)}',
    'nodeExtras': 'function(node) { node.append("text").attr("dx", 12).attr("dy", ".35em").text(function(d) { return d.name }); }'
    }

  __chartProp = {
    'dispatch': {'on': "'renderEnd', function(){console.log('render complete');}"}
  }

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s().%s ;
        %s
        d3.select("#%s svg").datum(%s).call(%s);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.htmlId)
    )
