"""

"""

from ares.Lib.html import AresHtmlContainer
from ares.Lib import AresItem
from ares.Lib import AresJs

class IndentedTree(AresHtmlContainer.GraphSvG):
  """
  data expected:
    [ (label, url, values), (label, url, dataKeys)]
    Example
    [ ('NVD3', 'http://novus.github.com/nvd3',
            [("Charts", None,
                [("Simple Line", "http://novus.github.com/nvd3/ghpages/line.html", {"type": "Historical"})])]),
      ("Chart Components", None, "Universal")]
  reference site: http://nvd3.org/examples/indentedtree.html
  """
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  showCount = 1
  alias = 'tree'

  def __init__(self, aresObj, cols, data):
    """

    cols should be a list of col and the col object should be defined like a dictionary with the below properties
      col = { key: 'type', label: 'Type', width: '25%', type: 'text' }
    """
    super(IndentedTree, self).__init__(aresObj, data)
    self.cols = cols

  def pyDataToJs(self):
    """ """
    return self.pyData[0]

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    return 'select("#chart%s")' % self.htmlId

  def jsChart(self):
    """ """
    return '''
              nv.models.indentedTree()
                .tableClass('table table-striped') //for bootstrap styling
                .columns([
                  {
                    key: 'key',
                    label: 'Name',
                    showCount: true,
                    type: 'text',
                    classes: function(d) { return d.url ? 'clickable name' : 'name' },
                    click: function(d) {if (d.url) window.location.href = d.url; }
                  },

                  // Section dedicated to the columns definition
                  {
                    key: 'type',
                    label: 'Type',
                    width: '25%',
                    type: 'text'
                  }

                ]);
          '''