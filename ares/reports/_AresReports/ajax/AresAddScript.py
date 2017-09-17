"""

"""

import os
import json
from ares import report

def call(aresObj):
  """

  """

  log = AresLog.AresLog(current_app.config['ROOT_PATH'], reportObj.http['report_name'], config)
  tmplPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'tmpl')

  scriptName, file_extension = os.path.splitext(reportObj.http['script'])
  if aresObj.http['script_type'] == 'Report':
    scriptName = report.getFileName(reportObj.http['script'], '.py')
    if scriptName is None:
      return json.dumps('Not script created, extension %s not recognised' % file_extension)

    shutil.copyfile(os.path.join(tmplPath, 'tmpl_report.py'), os.path.join(reportObj.http['DIRECTORY'], reportObj.http['report_name'], scriptName))
    log.addScript(reportObj.http['script_type'], scriptName)
    fileFullPath = os.path.join(reportObj.http['DIRECTORY'], reportObj.http['report_name'], scriptName)
    with zipfile.ZipFile("%s.zip" % fileFullPath, 'w') as zf:
      zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), scriptName))
    return json.dumps('New Script added: %s' % scriptName)

  elif reportObj.http['script_type'] == 'Python Service':
    ajaxPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, reportObj.http['report_name'], 'ajax')
    if not os.path.exists(ajaxPath):
      os.makedirs(ajaxPath)
      # Create also the init in order to be able to call the extra services directly
      initFile = open(os.path.join(ajaxPath, "__init__.py"), "w")
      initFile.close()

    scriptName = getFileName(reportObj.http['script'], '.py')
    if scriptName is None:
      return json.dumps('Not script created, extension %s not recognised' % file_extension)

    shutil.copyfile(os.path.join(tmplPath, 'tmpl_service.py'), os.path.join(reportObj.http['DIRECTORY'], reportObj.http['report_name'], 'ajax', scriptName))
    log.addScript(reportObj.http['script_type'], scriptName)
    fileFullPath = os.path.join(ajaxPath, scriptName)
    with zipfile.ZipFile("%s.zip" % fileFullPath, 'w') as zf:
      zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), scriptName))
    return json.dumps('New Script added: %s' % scriptName)

  elif reportObj.http['script_type'] == 'Javascript':
    scriptName = getFileName(reportObj.http['script'], '.js')
    if scriptName is None:
      return json.dumps('Not script created, extension %s not recognised' % file_extension)

    jsPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, reportObj.http['report_name'], 'js')
    if not os.path.exists(jsPath):
      os.makedirs(jsPath)
    newFile = open(os.path.join(jsPath, scriptName), "w")
    newFile.close()
    return json.dumps('New Script added: %s' % scriptName)

  elif reportObj.http['script_type'] == 'Configuration':
    scriptName = getFileName(reportObj.http['script'], '.json')
    if scriptName is None:
      return json.dumps('Not script created, extension %s not recognised' % file_extension)

    configPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, reportObj.http['report_name'], 'config')
    if not os.path.exists(configPath):
      os.makedirs(configPath)
    newFile = open(os.path.join(configPath, scriptName), "w")
    newFile.close()
    return json.dumps('New configuration file available: %s' % scriptName)

  return json.dumps("No Event %s defined..." % reportObj.http['script_type'])