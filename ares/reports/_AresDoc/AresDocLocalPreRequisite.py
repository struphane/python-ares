"""
"""

NAME = 'Local Run'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresObj.title("How to use AReS locally")
  aresObj.title2("What is ArES?")
  aresObj.paragraph("AReS is a Automatic Reporting Suite in Python which will allow you easily to display data from different sources. "
                    "The Lab will allow you to extend the environment by implementing in a shared and controlled place new component and the "
                     "AReS app will allow you to display those data using the best javascript and HTML frameworks !"
                    " Ares is a wrapper around those framework to easily and automatically generate HTML pages. Thanks to this App in the Lab,"
                    " it is possible to test your results locally, to share HTML pages but also to publish your scripts on the server (for validation)")
  aresObj.row([aresObj.img('tmpl_rpt.JPG'), aresObj.img("report_example.JPG")])
  aresObj.hr()

  aresObj.title2("Pre-requisite to set up your environment")
  aresObj.paragraph("Before reading the following part of this tutorial, please make sure that you have installed on your computer Python."
                    "AReS and the Lab are compatible with all the versions of Python and it does not require any further modules (except request) to run,"
                    " so please get a version of python using one of the following links {0}", htmlComp=[aresObj.externalLink('Python', "https://www.python.org/downloads/")])
  aresObj.paragraph("The server is running in 2.7 so if you use Python 3.x, please ensure that you are not using keywords or functions specific to this version"
                    "of python. You can also you other version of Python like Anaconda if you want to get all the Data Scientist modules installed directly."
                    "You can get the recommended version of Anaconda here: {0}", htmlComp=[aresObj.externalLink('Anaconda', 'https://www.anaconda.com/download/')])
  aresObj.paragraph("If you are using Python 2.7, you will have to install the request module in order to be able to psuh scripts on"
                    " the server. If you need help to install packages, please follow this link {0}", htmlComp=[aresObj.externalLink('request', "https://pypi.python.org/pypi/requests/2.7.0")])
  div = aresObj.div("In {0} you might have to set the proxy, so if this is needed plese follow the tutorial here {1}",
                          htmlComp=[aresObj.http['CONFIG']['COMPANY'], aresObj.externalLink('Proxy configuration', 'https://stackoverflow.com/questions/14149422/using-pip-behind-a-proxy')],
                          cssCls=['alert alert-info'])
  div.addAttr('role', 'alert')

  