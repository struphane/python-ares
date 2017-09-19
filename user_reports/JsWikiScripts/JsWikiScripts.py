"""

http://127.0.0.1:5000/reports/run/JsWikiScripts

"""

import os
import sys
import ajax.ajaxWikiRequest

NAME = "BDI Wiki Scripts"

def report(aresObj):
  """
  Entry point for the SPE script monitoring

  This page will be the entry point and it will return the comments for a given script.
  Those comments will then be potentially updated by users in order to improve the quality of the processes

  In this page only relevant information related to the documentation will be displayed to users.
  Scripts not migrated to the new framework, without the correct BDI standards, will not be available.

  """
  aresObj.title("Wiki Scripts")
  aresObj.title2("What is this section for ?")
  aresObj.paragraph('''
                      In this section you will be able to get some details about the scripts but also you will be able to
                      change them. This is very important because it will ensure a good understanding of the processes but
                      also it will help ensuring that the implementation is perfectly in line with the business needs.
                      
                      A transparency in the processes will help BDI to focus on the implementation but also will guarantee
                      a good and clear documentation. Do not hesitate to add comments in this section, they will then be
                      added to the production code.
                      
                      Do not worry your comments will not impact the production. Until the validation they are only stored 
                      in text files. The production environment is never updated directly.
                      
                      Please select a script and then press view comments
                    ''')
  input = aresObj.input("Script Name")
  aresObj.anchor('View Comments', **{'report_name': 'JsWikiScripts', 'script_name': 'JsWikiScriptCmmts', 'script': input})

  aresObj.title2("How many scripts are currently available ?")
  sys.path.append(aresObj.http['CONFIG']['WRK'])
  recordSet = []
  for file in os.listdir(aresObj.http['CONFIG']['WRK']):
    if file.endswith(".py"):
      scriptName = file.replace(".py", "")
      mod = __import__(scriptName)
      if hasattr(mod, 'BUSINESS'):
        recordSet.append({'scriptName': scriptName, 'total': 1, 'category': 'SPE Migrated'})
      else:
        recordSet.append({'scriptName': scriptName, 'total': 1, 'category': 'SPE Old'})

  pieChart = aresObj.pie(recordSet, [{'colName': 'Category', 'key': 'category'},
                                    {'colName': 'Count', 'key': 'total', 'type': 'number'}
                                    ], headerBox='Framework Migration')
  aresObj.paragraph('''
      Not all the scripts have been migrated to this new set up, but this is an on going process in BDI.
      So please have a look at the current documentation and do not hesitate to propose improvements.

      Also you can request for a script to be reviewed and migrated to the new framework.
      You request will be then taken into account and we will process it as part of our weekly comment review.
  ''')

  htmlList = aresObj.list(ajax.ajaxWikiRequest.getRequests(os.path.join(aresObj.http['DIRECTORY'], 'requests')), headerBox='Pending requests')
  aresObj.row([pieChart, htmlList])

  modal = aresObj.modal('Ask for a documentation review')
  modal.modal_header = "Request a Script Review"
  inputModal = aresObj.input("Script Name", '')
  reason = aresObj.textArea('')
  request = aresObj.button('Request')
  request.post('click', 'ares.ajaxCall', **{'report_name': 'JsWikiScripts', 'script': 'ajaxWikiRequest',
                                            'script_name': inputModal, 'comment': reason,
                                            'js': '''
                                                      display(status) ;
                                                      %s ;
                                                      %s.modal("toggle") ;
                                                  ''' % (htmlList.jsUpdate(), modal.jqId)})
  aresObj.addTo(modal, inputModal)
  aresObj.addTo(modal, reason)
  aresObj.addTo(modal, request)
  return aresObj
