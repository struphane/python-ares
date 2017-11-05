"""


"""
import sys
import os

NAMR = 'Pivot View'

def report(aresObj):
  """ View used only to display the content of a static cache """

  aresObj.title("Static Pivot View")
  aresObj.button("Save Changes")
  aresObj.newline()
  aresObj.newline()

  userDirectory = os.path.join(aresObj.http['DIRECTORY'], aresObj.http['user_report_name'])
  sys.path.append(userDirectory)
  module = __import__(aresObj.http['user_script_name'])
  for fileDef in getattr(module, 'FILE_CONFIGS', {}):
    if fileDef['filename'] == aresObj.http['static_file']:
      fileConfig = fileDef['parser']
      aresObj.files[fileDef['filename']] = fileConfig(open(
        os.path.join(aresObj.http['DIRECTORY'], aresObj.http['user_report_name'], fileDef['folder'],
                     fileDef['filename'])))
      recordSet = []
      for rec in aresObj.files[fileDef['filename']]:
        recordSet.append(rec)

      table = aresObj.table(recordSet, fileConfig.getHeader())
      table.callBackFooterColumns()
      table.dblClickOvr()

  sys.path.remove(userDirectory)
  for module, ss in sys.modules.items():
    if userDirectory in str(ss):
      del sys.modules[module]

  for f in aresObj.files.values():
    f.close()