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
import traceback

from ares.Lib import Ares

def getReport(results, directory, folder, reports, scriptPath):
  """ Recursively runs all the reports """
  mainreport = __import__(folder)
  extFiles = {}
  for extFile in getattr(mainreport, 'FILE_CONFIGS', {}):
    extFiles[extFile['filename']] = extFile
  for report in reports:
    reportName = report.replace(".py", "")
    if report.endswith(".py"):
      reportModule = __import__(reportName)
      if hasattr(reportModule, 'report'):
        print("  > Loading report %s" % report)
        results[reportModule.__name__] = Ares.Report()
        if hasattr(reportModule, 'HTTP_PARAMS'):
          for param in getattr(reportModule, 'HTTP_PARAMS'):
            results[reportModule.__name__].http[param['code']] = param['dflt']
        try :
          for f in ['static', 'outputs']:
            for file in os.listdir(os.path.join(directory, reportName, f)):
              if file in extFiles:
                inFile = open(os.path.join(directory, reportName, f, file))
                results[reportModule.__name__].files[file] = extFiles[file]['parser'](inFile)
          results[reportModule.__name__].http['DIRECTORY'] = scriptPath
          results[reportModule.__name__].http['REPORT_NAME'] = report.replace(".py", "")
          reportModule.report(results[reportModule.__name__])
        except Exception as e:
          print("Error with report %s" % report)
          print(traceback.print_exc())
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
  folder = "PivotTable" # The name of the main script with the report
  scripts = [
    'PivotTable.py',
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
  getReport(res, directory, folder, scripts, directoryPath)

  for report, htmlReport in res.items():
    htmlFile = open(r"%s\%s.html" % (path, report), "w")
    cssImports, jsImports, jsOnload, html, jsGraph, jsGlobal = htmlReport.html()
    htmlFile.write(Ares.htmlLocalHeader("%s\n%s" % (cssImports, cssImportsExtra), "%s\n%s" % (jsImports, jsImportsExtra), jsGlobal, jsOnload))
    htmlFile.write(html)
    htmlFile.write("\n<script>\n")
    htmlFile.write(jsGraph)
    htmlFile.write("\n</script>\n</div></div>")
    htmlFile.write(footer)
    htmlFile.close()
