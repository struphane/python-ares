"""
"""

import os
import re
import sys
import re
import collections
from flask_login import current_user
from flask import session
from ares.Lib import AresSql

regex = re.compile('[^a-zA-Z0-9_]')

from Libs import AresFileParser

CREATE_FILE_QUERY = '''REPLACE INTO file_map (alias, file_type, disk_name) VALUES ('%(fileCode)s', '%(file_type)s', '%(filename)s');
                      INSERT INTO file_auth (file_id, team_id, temp_owner)
                      SELECT file_map.file_id, team_def.team_id, '%(username)s'
                      FROM file_map, team_def
                      WHERE file_map.disk_name = '%(filename)s' and team_def.team_name = '%(team_name)s';'''

LOG_DEPLOY = '''INSERT INTO logs_deploy (email, team_name, folder, file, type)
                VALUES ("%(username)s", "%(team_name)s","%(report_name)s", "%(file)s", "%(type)s");'''

def call(aresObj):
  """

  """
  if not 'rows' in aresObj.http:
    tableAlias = 'datatable'
    pattern = re.compile("%s\[([0-9]*)\]\[([0-9a-zA-Z_]*)\]" % tableAlias)
    resultObj = collections.defaultdict(dict)
    for key, val in aresObj.http.items():
      if key.startswith(tableAlias):
        match = re.search(pattern, key)
        if match:
          resultObj[int(match.group(1))][match.group(2)] = val
    moduleName, className = aresObj.http['parserModule'].split(".")
    reportPath = os.path.join(aresObj.http['DIRECTORY'], aresObj.http['reportName'])
    sys.path.append(reportPath)

    try:
      __import__(aresObj.http['reportName'])
      mod = __import__("utils.%s" % moduleName)
      ajaxMod = getattr(getattr(mod, moduleName), className)
      recordSet = []
      if ajaxMod.hdrLines != 0:
        recordSet.append(dict([(col.get('key', regex.sub('', col['colName'])), col['colName']) for col in ajaxMod.cols]))
      rowNumers = max(resultObj.keys())
      for colIndex in range(rowNumers+1):
        recordSet.append(resultObj[colIndex])
      AresFileParser.saveFile(aresObj, aresObj.http['reportName'], recordSet, [col.get('key', regex.sub('', col['colName'])) for col in ajaxMod.cols],
                              ajaxMod.delimiter, aresObj.http['fileName'], ajaxMod.hdrLines, aresObj.http['folder'])


      db = AresSql.SqliteDB(aresObj.http['reportName'])
      fileParams = {'filename': aresObj.http['fileName'], 'fileCode': aresObj.http['static_code'], 'file_type': aresObj.http['folder'], 'username': current_user.email, 'team_name': session['TEAM']}
      db.modify(CREATE_FILE_QUERY % fileParams)
      queryParams = {'report_name': aresObj.http['reportName'], 'file': aresObj.http['fileName'], 'type': aresObj.http['folder'], 'username': current_user.email , 'team_name': session['TEAM']}
      db.modify(LOG_DEPLOY % queryParams)
    except Exception as e:
      return 'Problem during the update'

    finally:
      sys.path.remove(reportPath)
      for module, ss in dict(sys.modules).items():
        if reportPath in str(ss):
          del sys.modules[module]
  else:
    recordSet = []
    try:
      header = [col['key'] for col in AresFileParser.FilePivot.cols]
      for row in aresObj.http['rows'].split("\n"):
        recordSet.append(dict(zip(header, row.split(AresFileParser.FilePivot.delimiter))))
      AresFileParser.saveFile(aresObj, aresObj.http['reportName'], recordSet, [col.get('key', regex.sub('', col['colName'])) for col in AresFileParser.FilePivot.cols],
                              AresFileParser.FilePivot.delimiter, aresObj.http['fileName'], 1, aresObj.http['folder'])

    except:
      return 'Problem during the update'

  return 'File - %s - updated' % aresObj.http['fileName']