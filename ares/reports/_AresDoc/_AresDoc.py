""" Main Report for the AReS and the Lab documentation
"""

import collections
import os

NAME = 'Reports Documentation'
DOWNLOAD = None
SHORTCUTS = [('Local Runs', [
      ('Pre-requisite', 'AresDocLocalPreRequisite'),
      ('Set up', 'AresDocLocalSetUp'),
      ('First Script', 'AresDocLocalFirstScript'),
      ('Deployment', 'AresDocLocalDeploy'),
      #('HTML Components', 'AresDocHtml'),
      #('Graph Components', 'AresDocGraph'),
    ]
   )]

def report(aresObj):
  """ Function to produce the first entry point of the Documentation framework """
  aresObj.title("Python Lab Principal")
  aresObj.paragraph("Within this Open Framework, we are trying to give to any users the ability to"
                    " write small scripts and then to interact with the different modules available."
                    " This environment will give to people the ability to write scripts in order"
                    " to extract and tranform the data but also to visualise the data in a very"
                    " integrated manner. Some extra components are available in this framework to "
                    " help on embedding the extraction but also the web visualisation. Thus"
                    " thanks to this framework you will succeed in the below points !")
  aresObj.title3(" No need to learn a new language or no dependency on a module ")
  val = aresObj.paragraph("Different simple components already wrapped in python to step in very quickly."
                          " Framework compatible with both Python 2.7 and up. Modules documented and split to allow"
                          " you or your IT teams to fully customize it for your business needs")
  moreDetails = aresObj.href("Get more details", "_AresDocPython")
  aresObj.row([aresObj.col([val, moreDetails]), aresObj.img('tmpl_rpt.JPG')])
  aresObj.title3(" Be more productive and be an actor in your system ")
  val1 = aresObj.paragraph("Re use any D3 or bespoke charts to display your information in a dynamic manner"
                           " transform the data using directly your local scripts. Propose a new collaborative way"
                           " to produce team dashboards")
  val2 = aresObj.paragraph(" Easy to add or change new Javascript and CSS components. Everything is dynamically"
                           " managed by the python layer. All the components used are defined in the AresJsModules.py. "
                           " Each reports and modules can be downloaded from the web interface and can then be run locally")
  title = aresObj.title4(" Give an new dimension to your local simple scripts", cssAttr={'font-weight': 'bold', 'text-align': 'center'})
  moreDetails = aresObj.href("Get more details", "_AresDocReport")
  aresObj.row([aresObj.img('d3_components.JPG'), aresObj.col([val1, val2, title, moreDetails])])

  aresObj.title3(" Link all the components within your IT company ")
  val1 = aresObj.paragraph("As today most of the legacy systems have REST API it is quite easy with python modules "
                           "to extract information from them. Also it is possible to import natively C / C++ modules"
                           " from the platform. No need for extra development work, each team can implement the link to"
                           " this centralise system")
  moreDetails = aresObj.externalLink("Get to Python website", "https://docs.python.org/3/c-api/index.html")
  title = aresObj.title4(" Benefit from the community of users", cssAttr={'font-weight': 'bold', 'text-align': 'center'})
  aresObj.row([aresObj.col([val1, title, moreDetails]), aresObj.img('link_components.JPG')])

