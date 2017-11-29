""" [SCRIPT COMMENT]

>>>> Important variables / functions

from math import cos as cos
from math import sin as sin

In the python layer
    aresObj.http['FILE'] is the current file
    aresObj.http['REPORT_NAME'] is the current report environment name
    aresObj.http['DIRECTORY'] is the report location

     def readFile(self, file, subfolders=None):
     def createFile(self, file, subfolders=None, checkFileExist=True):
     def getFolders(self):
     def getFiles(self, subfolders):


In the javascript layer
    display(data) to return the result in a notification modal popup
    preloader() to show a loading page

"""


NAME = 'Volatility surface' # The Report Name in the left menu
# The Shortcuts should be defined as below
# [(Cateogry Name, [List of the script in the root directory])]
# It is only possible to create new links for scripts in the root
SHORTCUTS = [] # All the possible link to other pages
FILE_CONFIG = [] # All the static and output files configurationa
# The format in the above list should be as: {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},

HTTP_PARAMS = [] # If you want to use the param method to set parameter before running hte report

import random

#def params(aresObj):
#  """ Optional param method to be run before the report method to set parameter """

from math import cos
from math import sin


def report(aresObj):
  '''
  Write your function below
  '''


  """    var counter = 0;
    var steps = 50;  // number of datapoints will be steps*steps
    var axisMax = 314;
    var axisStep = axisMax / steps;
    for (var x = 0; x < axisMax; x+=axisStep) {
        for (var y = 0; y < axisMax; y+=axisStep) {
            var value = (Math.sin(x/50) * Math.cos(y/50) * 50 + 50);
            data.add({id:counter++,x:x,y:y,z:value,style:value});"""
  counter = 0
  recordSet = []
  axisMax = 314
  steps = 50
  axisStep = int(axisMax / steps)
  x = 0
  while (x < axisMax):
    y = 0
    while (y < axisMax):
      value = (sin(x/50) * cos(y/50) * 50 + 50)
      recordSet.append({'id': counter, 'x':x, 'y':y, 'z':value, 'style':value})
      counter += 1
      y += axisStep
    x += axisStep


  title = aresObj.title("Volatility surface example")
  title.hidden = True
  # Example of DropDown selection
  #   - parameter 1: the title to be displayed in the object
  #   - parameter 2: the content of the dropdown (the items should be tuple (Name, hyperlink)
  aresObj.newline()
  aresObj.newline()
  aresObj.newline()
  surface = aresObj.vis3DSurface(recordSet)

  surface.hidden = True
  surface.setDataSet(recordSet)

  venn = aresObj.venn(recordSet, [], mockData=True, inReport=False)

  div = aresObj.div()
  button = aresObj.button('Click')
  button.loadTo(venn, div)
