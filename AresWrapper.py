""" Local wrapper to be able to produce static reports locally without server

From this mode the framework will generate a static html page.
This will allow to produce statics reports and to share the page even without any access to the network

Some external Javascript and CSS libraries are required to be able to run the tool fully locally

Do not use True in both python and Javascript as the Json conversion is not really optimal. Please use boolean instead
"""

import os
import sys
import Ares

# CSS imports
CSS = ['jquery-ui.css',
       'bootstrap.css',
       'bootstrap.min.css',
       'bootstrap-theme.min.css',
       'nv.d3.css',
       'bootstrap-select.min.css'
       ]

# Javascript imports
JS = ['jquery-3.2.1.min.js',
      'jquery-ui.min.js',
      'bootstrap.min.js',
      'bootstrap-select.min.js',
      'd3.v3.js',
      'nv.d3.js', # The mimifyed version does not contain indentedTree objects. https://stackoverflow.com/questions/35452946/not-running-minimal-example-of-indentedtree
      'd3.layout.cloud.js' # world cloud chart
      ]

def components(directory):
  """ Return the list of all the available components """
  import inspect
  import Ares
  import AresHtml
  import AresGraph

  htmlObject = []
  for name, obj in inspect.getmembers(AresHtml):
    if inspect.isclass(obj) and obj.alias is not None:
      htmlObject.append((name, obj.__doc__))

  htmlFile = open(r"%s\ArES_components.html" % directory, "w")
  aresObj = Ares.Report()
  aresObj.title(2, "Html Components")
  aresObj.table(['Class Name', 'Description'], htmlObject)


  graphObject = []
  for name, obj in inspect.getmembers(AresGraph):
    if inspect.isclass(obj):
      graphObject.append((name, obj.__doc__))
  aresObj.title(2, "Graph Components")
  aresObj.table(['Class Name', 'Description'], graphObject)

  htmlPage(htmlFile, aresObj.html(directory, title='ArES Components'))

  htmlFile.close()
  sys.exit()

def test(className, directory):
  """ Test a component based on Mock Json data

  """
  import Ares
  import AresGraph
  import AresHtml
  import inspect
  import json

  aresComponents = {}
  for name, obj in inspect.getmembers(AresHtml):
    if inspect.isclass(obj):
      aresComponents[name] = obj
  for name, obj in inspect.getmembers(AresGraph):
    if inspect.isclass(obj):
      aresComponents[name] = obj

  htmlFile = open(r"%s\ArES_%s.html" % (directory, className), "w")
  aresObj = Ares.Report()
  aresObj.title(2, "%s Components" % className)
  object = aresComponents[className]
  aresObj.text(object.__doc__)
  with open(r"%s\%s" % (directory, object.mockData)) as data_file:
    data = json.load(data_file)
  aresObj.comboLineBar(data)

  aresObj.title(2, 'Source Code')
  aId = aresObj.anchor('Data Source', object.mockData)
  aresObj.paragraph('You can download the input data here: {0}', [aresObj.item(aId)])

  compObj = aresComponents[className](0, data)
  aresObj.code(compObj.js())
  htmlPage(htmlFile, aresObj.html(directory, title='ArES Components'))

  htmlFile.close()
  sys.exit()


if __name__ == '__main__':
  # Run the script locally

  statisPath = r'' # the path with the CSS and JS folders (if current path please keep this empty
  directory = os.getcwd() # The path of this script by default
  report = "MyRepotTest" # The name of the main script with the report

  # -----------------------------------------------------------------------------------------------
  # Test functions
  # -----------------------------------------------------------------------------------------------
  # Get a description of the different available items
  #components(directory)
  #test('ComboLineBar', directory)


  # Write the report
  htmlPage = Ares.htmlLocalHeader(directory, report, statisPath, CSS, JS)
  htmlPage.write(__import__(report).report(Ares.Report(), localPath=directory))
  Ares.htmlLocalFooter(htmlPage)



