""" Local wrapper to be able to produce static reports locally without server

From this mode the framework will generate a static html page.
This will allow to produce statics reports and to share the page even without any access to the network

Some external Javascript and CSS libraries are required to be able to run the tool fully locally

Do not use True in both python and Javascript as the Json conversion is not really optimal. Please use boolean instead

Ares documentation is available here:
  http://127.0.0.1:5000/reports/doc
[This documentation is autogenerated from the script comments]

"""

from __future__ import print_function
import os
import sys

from ares.Lib import Ares

def getReport(results, reports, scriptPath):
  """ Recursively runs all the reports """
  for report in reports:
    if report.endswith(".py"):
      reportModule = __import__(report.replace(".py", ""))
      if hasattr(reportModule, 'report'):
        print("  > Loading report %s" % report)
        results[reportModule.__name__] = Ares.Report()
        results[reportModule.__name__].http['DIRECTORY'] = scriptPath
        results[reportModule.__name__].http['REPORT_NAME'] = report.replace(".py", "")
        try:
          reportModule.report(results[reportModule.__name__])
        except Exception as e:
          print("Error with report %s" % report)
          print(e)
      else:
        print("Module ignore %s" % report)



if __name__ == '__main__':
  # Run the script locally

  result_folder = 'html'
  serverStatics = True # To supply you statics folder with your versions of the CSS and Js files
  directory = os.getcwd() # The path of this script by default
  # This will move all the results in a html folder
  # It only work locally
  folder = "NewReport" # The name of the main script with the report
  scripts = [
    'NewReport.py',
    ]

  path = os.path.join(directory, result_folder, folder)
  if not os.path.exists(path):
    os.makedirs(path)

  cssPath = os.path.join(directory, folder, 'styles')
  cssImportsExtra = []
  if os.path.exists(cssPath):
    for cssFile in os.listdir(cssPath):
      if cssFile.endswith('.css'):
        cssImportsExtra.append('<link rel="stylesheet" href="../../%s/styles/%s">' % (folder, cssFile))
  cssImportsExtra = "\n".join(cssImportsExtra)

  jsPath = os.path.join(directory, folder, 'styles')
  jsImportsExtra = []
  if os.path.exists(jsPath):
    for jsFile in os.listdir(jsPath):
      if jsFile.endswith('.js'):
        jsImportsExtra.append('<script language="javascript" type="text/javascript" src="../../%s/styles/%s"></script>' % (folder, jsFile))
  jsImportsExtra = "\n".join(jsImportsExtra)

  # Create the generic headers and footers
  footer = Ares.htmlLocalFooter()

  res = {}
  directoryPath = os.path.join(directory, folder)
  sys.path.append(directoryPath)
  ajaxPath = os.path.join(directory, folder, 'ajax')
  if os.path.exists(ajaxPath):
    sys.path.append(ajaxPath)
  getReport(res, scripts, directoryPath)

  for report, htmlReport in res.items():
    htmlFile = open(r"%s\%s.html" % (path, report), "w")
    cssImports, jsImports, jsOnload, html, js = htmlReport.html()
    htmlFile.write(Ares.htmlLocalHeader("%s\n%s" % (cssImports, cssImportsExtra), "%s\n%s" % (jsImports, jsImportsExtra), jsOnload))
    htmlFile.write(html)
    htmlFile.write("\n<script>\n")
    htmlFile.write(js)
    htmlFile.write("\n</script>\n</div></div>")
    htmlFile.write(footer)
    htmlFile.close()
