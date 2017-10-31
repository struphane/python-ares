r""" Simple wrapper to create a new environment locally

This will directly build the right set up and then it will be easier to start designing your framework
The structure of your environment should be as follow

\YouFolderName
  YouFolderName.py # The main script runs when you enter to your environment
  YourReport2.py # A second report which can be linked to the main one in the side bar
  ...
  YourReportN.py # A Nth report which can be linked to the main one in the side bar

  \styles # Some CSS or Javascript files that you need to run your report
    newtest.js
    newtest.css

  \ajax # Some Python script services which should be used to update part of the reports
    __init__.py
    ajaxService1.py

  \outputs # All the text files that your script will produce

  \saved # The html reports generated by running the scripts locally
    xxx.html # you can push those result files locally to then share them

  \utils # All the common modules needed to run the reports and the services in your framework
    __init__.py
    libReport.py

  \statics # All the static files required to run your report

"""

import os
import shutil

if __name__ == '__main__': # To be run directly
  # This script should be placed at the root
  reportName = 'NewReport' # THis will be the name of your environment (your folder)
  removeExistingFilder = True
  # In your environment you can have multiple folders and services

  # Then creation of the dummy report environment
  if os.path.exists(reportName) and removeExistingFilder:
    shutil.rmtree(reportName)

  if not os.path.exists(reportName):
    os.makedirs(reportName)
  # Create the sub folders
  for subFolder in ['ajax', 'statics', 'outputs', 'styles', 'saved', 'utils']:
    if not os.path.exists(os.path.join(reportName, subFolder)):
      os.makedirs(os.path.join(reportName, subFolder)) # for the javascript fragments
      if subFolder in ['ajax', 'utils']:
        # Create the init file neeeded to import the modules
        open(os.path.join(reportName, subFolder, '__init__.py'), 'w').close()
  if not os.path.exists(os.path.join(reportName, '%s.py' % reportName)):
    open(os.path.join(reportName, '%s.py' % reportName), 'w').close()
