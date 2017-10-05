"""

"""

from ares.Lib.html import AresHtmlContainer


class NvD3Tree(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'tree', 'indentedTree'
  chartStyle = {'tableClass': '"table table-striped"'}

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def dataFnc(self):
    """ """
    return '''
          [{
              key: 'NVD3',
              url: 'http://novus.github.com/nvd3',
              values: [
                {
                  key: "Charts",
                  _values: [
                    {
                      key: "Simple Line",
                      type: "Historical",
                      url: "http://novus.github.com/nvd3/ghpages/line.html"
                    },
                    {
                      key: "Scatter / Bubble",
                      type: "Snapshot",
                      url: "http://novus.github.com/nvd3/ghpages/scatter.html"
                    },
                    {
                      key: "Stacked / Stream / Expanded Area",
                      type: "Historical",
                      url: "http://novus.github.com/nvd3/ghpages/stackedArea.html"
                    },
                    {
                      key: "Discrete Bar",
                      type: "Snapshot",
                      url: "http://novus.github.com/nvd3/ghpages/discreteBar.html"
                    },
                    {
                      key: "Grouped / Stacked Multi-Bar",
                      type: "Snapshot / Historical",
                      url: "http://novus.github.com/nvd3/ghpages/multiBar.html"
                    },
                    {
                      key: "Horizontal Grouped Bar",
                      type: "Snapshot",
                      url: "http://novus.github.com/nvd3/ghpages/multiBarHorizontal.html"
                    },
                    {
                      key: "Line and Bar Combo",
                      type: "Historical",
                      url: "http://novus.github.com/nvd3/ghpages/linePlusBar.html"
                    },
                    {
                      key: "Cumulative Line",
                      type: "Historical",
                      url: "http://novus.github.com/nvd3/ghpages/cumulativeLine.html"
                    },
                    {
                      key: "Line with View Finder",
                      type: "Historical",
                      url: "http://novus.github.com/nvd3/ghpages/lineWithFocus.html"
                    }
                  ]
                },
                {
                  key: "Chart Components",
                  _values: [
                    {
                      key: "Legend",
                      type: "Universal",
                      url: "http://novus.github.com/nvd3/examples/legend.html"
                    }
                  ]
                }
              ]
            }]

        '''

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
      ''' % (self.htmlId, self.chartObject, "\n.".join(chartAttributes),
             self.jqId, self.htmlId, self.dataFnc(), self.htmlId)
    )