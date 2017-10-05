"""

"""

from ares.Lib.html import AresHtmlContainer


class NvD3Tree(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'tree', 'indentedTree'
  __chartStyle = {'tableClass': '"table table-striped"'}
  references = ['http://nvd3.org/examples/indentedtree.html']

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s
            .columns([
                  {
                    key: 'key',
                    label: 'Name',
                    showCount: true,
                    width: '75%%',
                    type: 'text',
                    classes: function(d) { return d.url ? 'clickable name' : 'name' },
                    click: function(d) {
                       if (d.url) window.location.href = d.url;
                    }
                  },
                  {
                    key: 'type',
                    label: 'Type',
                    width: '25%%',
                    type: 'text'
                  }
                ]);

        %s.remove() ;
        d3.select("#%s").datum(%s)
          .call(%s);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(),
             self.jqId, self.htmlId, self.dataFnc(), self.htmlId)
    )