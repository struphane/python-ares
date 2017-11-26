""" Chart module in charge of generating a Spider Chart
@author: Olivier Nogues

"""
#TODO Add the legend

import json
# from Libs import AresChartsService

from ares.Lib import AresHtml


class Vis3DSurfaceChart(AresHtml.Html):
  """ NVD3 Spider Chart python interface """
  alias = '3dSurface'

  reqJs = ['vis']
  reqCss =  ['vis']
  series = None
  width = '500px'
  height = '550px'

  def setDataSet(self, recordSet):
    """ """
    self.recordSet = "%s" % json.dumps(recordSet)

  def __str__(self):
    """Standard function to return the html representation of a 3d surface chart"""
    return '''
              <div id="visualization_%s"></div>
              <script type="text/javascript">
                  // Create and populate a data table.
                  var data = new vis.DataSet();
                  // create some nice looking data with sin/cos
                  var aresDataSet = %s;
                  var arrayLength = aresDataSet.length; 
                  console.log(arrayLength);

                  for (var i =0; i < arrayLength; i++){
                    console.log(aresDataSet[i]);
                    data.add(aresDataSet[i]);
                      }
                  
              
                  // specify options
                  var options = {
                      width:  '%s',
                      height: '%s',
                      style: 'surface',
                      showPerspective: true,
                      showGrid: true,
                      showShadow: false,
                      keepAspectRatio: true,
                      verticalRatio: 0.5
                  };
              
                  // Instantiate our graph object.
                  var container = document.getElementById('visualization_%s');
                  var graph3d = new vis.Graph3d(container, data, options);
              </script>


            ''' % (self.htmlId, self.recordSet, self.width, self.height, self.htmlId)

