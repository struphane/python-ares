""" Local wrapper to be able to produce static reports locally without server

From this mode the framework will generate a static html page.
This will allow to produce statics reports and to share the page even without any access to the network

Some external Javascript and CSS libraries are required to be able to run the tool fully locally

Do not use True in both python and Javascript as the Json conversion is not really optimal. Please use boolean instead
"""

import os
from Lib import Ares


# CSS imports
CSS = ['jquery-ui.css',
       'bootstrap.min.css',
       'bootstrap-theme.min.css',
       'nv.d3.css',
       'bootstrap-select.min.css',
       #'svg.css'
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


def getReport(reportModule, results, scriptPath):
  """ Recursively runs all the reports """
  print("  > Running report %s" % reportModule.__name__)
  aresObj = Ares.Report()
  aresObj.http['USER_PATH'] = scriptPath
  results[reportModule.__name__] = reportModule.report(aresObj)
  for child in getattr(reportModule, 'CHILD_PAGES', {}).values():
    getReport(child.replace(".py", ""), results, scriptPath)


if __name__ == '__main__':
  # Run the script locally
  statisPath = r'..\..\..\static' # the path with the CSS and JS folders (if current path please keep this empty
  directory = os.getcwd() # The path of this script by default
  report = "report_index" # The name of the main script with the report
  result_folder = 'html'

  # This will move all the results in a html folder
  # It only work locally
  path = os.path.join(directory, result_folder, report)
  if not os.path.exists(path):
    os.makedirs(path)
  if not statisPath:
    localPathSize = len(os.path.split(path))
    if os.path.split(path)[0] == '':
      localPathSize -= 1
    statisPath = os.path.join(*[".." for i in range(localPathSize)])

  # Create the generic headers and footers
  header = Ares.htmlLocalHeader(statisPath, CSS, JS)
  footer = Ares.htmlLocalFooter()

  res = {}
  getReport(__import__(report), res, directory)

  for report, htmlReport in res.items():
    htmlFile = open(r"%s\%s.html" % (path, report), "w")
    jsOnload, html, js = htmlReport.html()
    htmlFile.write(header)
    htmlFile.write("\n  <script>\n")
    htmlFile.write(jsOnload)
    htmlFile.write("\n  </script>\n</head>\n<body>\n<div class='container' id='html_content'>\n")
    htmlFile.write(html)
    htmlFile.write("\n<script>\n")
    htmlFile.write(js)
    htmlFile.write("\n</script>\n</div>")
    htmlFile.write(footer)
    htmlFile.close()






