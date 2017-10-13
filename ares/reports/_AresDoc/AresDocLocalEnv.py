"""
"""

NAME = 'Local Run'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresObj.title("How to use ArES locally")
  aresObj.title2("What is ArES?")
  aresObj.paragraph("AReS is a Automatic Reporting Suite in Python which will allow you easily to display data from different sources. "
                    "The Lab will allow you to extend the environment by implementing in a shared and controlled place new component and the "
                     "AReS app will allow you to display those data using the best javascript and HTML frameworks !"
                    " Ares is a wrapper around those framework to easily and automatically generate HTML pages. Thanks to this App in the Lab,"
                    " it is possible to test your results locally, to share HTML pages but also to publish your scripts on the server (for validation)")
  aresObj.row([aresObj.img('tmpl_rpt.JPG'), aresObj.img("report_example.JPG")])
  aresObj.hr()

  aresObj.title2("Rre-requisite to set up your environment")
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
  aresObj.hr()
  aresObj.title2("Set up your environment")
  aresObj.title4("Using the install")
  content1 = aresObj.paragraph("Using this method you only have to run using your python version the script."
                               "This script will run a query on the server and it will retrieve the full package."
                               "The version of the scripts using this REST service will guarantee a correct synchronisation "
                               "with the server")
  content2 = aresObj.paragraph("Once the installation is completed, the ares folder with all the modules used to produce"
                               " HTML components will be downloaded. You can also find a example of project structure that "
                               "ares will recognise. ")
  aresObj.row([aresObj.col([content1,
                            aresObj.newline(),
                            aresObj.img("install_run.JPG"),
                            aresObj.newline(),
                            content2]),
               aresObj.col([aresObj.img("install_script.JPG"),
                            aresObj.newline(),
                            aresObj.img("install_result.JPG")])])

  aresObj.title4("Manual configuration")
  content1 = aresObj.paragraph("The Framework is very easy to set up and it will allow to perform all the tests fully locally based on your environment "
                              "but it will allow you also to deploy your scripts easily on the server. The only thing required is to click on the Download AReS link "
                              "{0}, to unzip the archive in a folder and then to start writing your first Python codes in a folder.", htmlComp=[aresObj.href("AReS", '', cssCls=[])])
  content2 = aresObj.paragraph("Using this way you will get the same environment except that the NewReport folder will not be generated."
                               "This folder is not very useful, it will just help you on understanding the structure of a project.")
  downloadPicture = aresObj.img('ares_download.JPG')
  aresObj.row([aresObj.col([content1, content2]), downloadPicture])
  aresObj.hr()

  aresObj.title2("How to create and run your first script")
  aresObj.paragraph('''
                        First of all create a folder with the name of your report. This name should be the name of the main script of your environment.
                        Indeed it will be the entry point to go thought your pages interactively. <BR />
                        Then copy the from the Lib folder to your folder and rename it. This will give you the standard format
                        expected by the framework.

                    ''')
  localEnv = aresObj.img('first_report_1.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_2.JPG')
  downloadPicture.doubleDots = 2
  #aresObj.table('', [['', ''], [localEnv, downloadPicture]])

  aresObj.paragraph('''
                        Then add the different HTML components to your reports !!! <BR />
                        Once your report created you can run it locally and get the result in a HTML file
                    ''')
  localEnv = aresObj.img('first_report_3.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_4.JPG')
  downloadPicture.doubleDots = 2
  #aresObj.table('', [['Create your report', 'Run the Wrapper in your IDE'], [localEnv, downloadPicture]])

  localEnv = aresObj.img('first_report_5.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_6.JPG')
  downloadPicture.doubleDots = 2
  #aresObj.table('', [['Get the file', 'Open it in your web browser'], [localEnv, downloadPicture]])

  aresObj.paragraph('''
                        Then once your report is finalised your can upload it to our server and share it with other user. <BR />
                        The module AresWrapperDeploy.py will allow the connection with the server. The creation of files, folder and
                        also the check of the version of your locally framework are done from script. <BR />
                        All new features and modules developed on the server will be available either from pip or directly in the zip
                        archive for simple tools.
                    ''')
  localEnv = aresObj.img('first_report_7.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_8.JPG')
  downloadPicture.doubleDots = 2
  #aresObj.table('', [['Push to the server', 'Environment Available'], [localEnv, downloadPicture]])

  aresObj.title4("Your script will be avaiable !!!")
  localEnv = aresObj.img('first_report_9.JPG')
  localEnv.doubleDots = 2
  aresObj.newline()
  aresObj.newline()


  aresObj.title4("Example of Python to HTML transform")
  localEnv = aresObj.img('html_python.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('html_example.JPG')
  downloadPicture.doubleDots = 2
  #aresObj.table('', [['Python Code', 'HTML result'], [localEnv, downloadPicture]])

  aresObj.newline()
  aresObj.title4("Example of Python to Javascript / Ajax transform")
  localEnv = aresObj.img('javascript_python.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('javascript_example.JPG')
  downloadPicture.doubleDots = 2
  #aresObj.table('', [['Python Code', 'Javascript Result'], [localEnv, downloadPicture]])

  aresObj.paragraph('''
                        More details on the components are available on the below links
                    ''')
  #aresComp = aresObj.anchor('HTML Component documentation')
  #aresComp.addLink('html', dots='..')
  aresObj.newline()
  #aresComp = aresObj.anchor('Graph Component documentation')
  #aresComp.addLink('graph', dots='..')

  aresObj.title3("Available Modules")
