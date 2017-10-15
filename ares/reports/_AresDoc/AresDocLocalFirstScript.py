"""
"""

NAME = 'Local Run'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresObj.title("How to create and run your first script")
  aresObj.paragraph("First of all you wiil have to create a folder with the name of your report. This name should be the name of "
                    "the main script of your environment. Indeed the framework will consider it as the entry point to go thought"
                    " your pages interactively. You will be able after to create some link with other reports or services fro this page.")
  aresObj.paragraph("Any valid report in the framework should have a {0} function and should pass the {1}. This function is"
                    " the one called by the Lab directly. It will add the different HTML and javascript logic to your aresObj"
                    " in order to later on construct your page. If you want more details about the AReS components, please have a "
                    "loot at the HTML and Chart documentation or directly check the implementation of the {2} module.",
                    htmlComp=[aresObj.text("report", cssAttr={"font-weight": 'bold', 'color': 'red'}),
                              aresObj.text("aresObj", cssAttr={"font-weight": 'bold', 'color': 'red'}),
                              aresObj.code("Ares.py")])

  content = aresObj.paragraph("For example on the right you can see the definition locally of a new environment HelloWorld"
                              " This environment will be defined at the root and within this folder we created a HelloWorld.py "
                              "script")
  div = aresObj.div("Please make sure that the name of your environment is generic enough and can group multiple reports."
                    "It is better to create a set of reports and services in the same folder ", cssCls=['alert alert-info'])
  div.addAttr('role', 'alert')
  dataInReport = aresObj.img('first_report_3.JPG')
  localEnv = aresObj.img('first_report_1.JPG')
  downloadPicture = aresObj.img('first_report_2.JPG')
  aresObj.row([aresObj.col([content, div, dataInReport]), aresObj.col([localEnv, downloadPicture])])

  aresObj.paragraph("By using the framework and the AresIntall script you will get an full example of structure expected "
                    "for a report. Indeed even if all the reports should be defined in the folder root, some other directories"
                    " can be used to get more flexibilities in the enviroments.")


  table = aresObj.simpletable([{'NAME': 'ajax', 'DSC': 'Folder with all the python scripts "services" used to extract the data from '
                                               'a source'},
                       {'NAME': 'js', 'DSC': 'Folder with all the javascript fragments. Some HTML components can load javascript'
                                             ' fragments. Those modules are not expecting functions but just some lines of javascript'},
                       {'NAME': 'json', 'DSC': 'Folder with the static configuration. It is possible to load those data from a report'
                                               'directly. A report is not expected to write to this folder, data should only read only.'},
                       {'NAME': 'outputs', 'DSC': 'Output folder for your reports. Functions are available in the aresObj to read and '
                                                  'write files in this directory'},
                       {'NAME': 'saved', 'DSC': 'Folder dedicated to store html files. Possibility to upload html files generated locally'
                                                ' and to share them with other teams'},
                       {'NAME': 'statics', 'DSC': 'Folder with all the external tools configuration'},
                       {'NAME': 'styles', 'DSC': 'Folder with the extra CSS and JS needed in the header.'},
                       ],
                      [{'key': 'NAME', 'colName': 'Folder Name'},
                       {'key': 'DSC', 'colName': 'Folder Description'}]
                      , cssAttr={'border': '1px solid black'})
  aresObj.row([aresObj.img('first_script_setup.JPG')])

  content1 = aresObj.paragraph(" Then you can add the different HTML components to your report. For the time being the "
                               "easiest way to do this would be to use the Ares.py module to see all the function available"
                               " and the parameter required (A documentation is currently in progress).")
  content2 = aresObj.paragraph(" Some keywords are important to correctly configure your report")
  listdata = aresObj.list(['NAME, is the name of the report on the left hand side',
                           'SHORTCUTS, are the list of sub reports attached to this one per categories'],
                          cssCls=['tick'])

  content3 = aresObj.paragraph("Also the below variable will be available in the aresobj")
  listdata2 = aresObj.list(["aresObj.http['DIRECTORY'], your folder directory",
                            "aresObj.http['FILE'], your current script",
                            "aresObj.http['REPORT_NAME'], your current folder name",
                            "aresObj.http[XXX], all your GET and POST variables. Those variables will be defined"
                            "in uppercase"
                            ], cssCls=['tick'])
  aresObj.row([aresObj.col([content1, content2, listdata, content3, listdata2]),
               aresObj.img('first_script_python.JPG')])


  aresObj.paragraph("Once your report is defined and available, you can use the next script in your local "
                    "environment {0} to test the HTML result. Basically you can run this script and it will "
                    "produce in the same directory a HTML folder with the output. For example the above local "
                    "report will produce locally the below page. You can use your web browser to get the result "
                    "expected on the server. Make sure that your folder refers to the name of your local "
                    "environment and that the list of scripts is the one you want to test. You can test multiple"
                    " reports locally, but please be aware that any service cannot be called locally, they have to "
                    " be deployed on the server to be used",
                    htmlComp=[aresObj.code("AresLocalRuns.py")])
  aresObj.row([aresObj.img('first_script_local_run.JPG'),
               aresObj.img('first_report_result.JPG')])