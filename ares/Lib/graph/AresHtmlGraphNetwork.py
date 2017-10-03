"""

"""

from ares.Lib.graph import AresHtmlGraph

class Network(AresHtmlGraph.JsNvD3Graph):
  """

  Reference website: https://github.com/nylen/d3-process-map
  """
  mockData = r'json\mapGraph.json'
  alias = 'network'

  def js(self, localPath=None):
    """ Return the entries to be added to the Javascript to create the graph during the loading """
    res = ["%svar config = %s ;\n" % self.pyDataToJs(localPath)]
    return "\n".join(res)