"""
"""

NAME = 'Local Run'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresObj.title("How to create and run your first script")
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
