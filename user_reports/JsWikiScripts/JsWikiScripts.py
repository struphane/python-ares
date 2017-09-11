"""

http://127.0.0.1:5000/reports/run/JsWikiScripts

"""


def report(aresObj):
  """

  """
  aresObj.title("Wiki Scripts")
  aresObj.title2("What is this section for ?")
  aresObj.paragraph('''
                      In this section you will be able to get some details about the scripts but also you will be able to
                      change them. This is very important because it will ensure a good understanding of the processes but
                      also it will help ensuring that the implementation is perfectly in line with the business needs.
                      
                      A transparency in the processes will help BDI to focus on the implementation but also will guarantee
                      a good and clear documentation. Do not hesitate to add commments in this section, they will then be
                      added to the production code.
                      
                      Do not worry your comments will not impact the production. Until the validation they are only stored 
                      in text files. The production environment is never updated directly.
                      
                      Please select a script and then press view comments
                    ''')
  input = aresObj.input("")
  aresObj.anchor('View Comments', **{'report_name': 'JsWikiScripts', 'script_name': 'JsWikiScriptCmmts', 'script': input})
  return aresObj
