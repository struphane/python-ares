"""

"""

import sys
import os

NAMR = 'Static View'

def report(aresObj):
  """ View used only to display the content of a static cache """

  aresObj.title("Static configuration View")
  input = aresObj.input('FileName')
  input.addVal(aresObj.http['static_file'])
  saveButton = aresObj.savetable("Save Changes")
  aresObj.newline()
  aresObj.newline()

  userDirectory = os.path.join(aresObj.http['DIRECTORY'], aresObj.http['user_report_name'])
  sys.path.append(userDirectory)
  module = __import__(aresObj.http['user_script_name'])
  for fileDef in getattr(module, 'FILE_CONFIGS', {}):
    if fileDef['filename'] == aresObj.http['static_file']:
      fileConfig = fileDef['parser']
      aresObj.files[fileDef['filename']] = fileConfig(open(os.path.join(aresObj.http['DIRECTORY'], aresObj.http['user_report_name'], fileDef['folder'], fileDef['filename'])))
      recordSet = []
      for rec in aresObj.files[fileDef['filename']]:
        recordSet.append(rec)

      table = aresObj.table(recordSet, fileConfig.getHeader(), headerBox="Static File - %s" % aresObj.http['static_file'], cssAttr={'width': '600px'})
      table.callBackFooterColumns()

  sys.path.remove(userDirectory)
  for module, ss in sys.modules.items():
    if userDirectory in str(ss):
      del sys.modules[module]

  for f in aresObj.files.values():
    f.close()

  if aresObj.http['file_parser'] != '':
    table.allowOverride()
    aresObj.http['REPORT_NAME'] = aresObj.http['user_report_name']
    saveButton.clickStatic(table, aresObj.http['file_parser'], input.val)
  else:
    saveButton.disable = True