"""

"""

from ares.Lib import AresSql
from Libs import mailer


NAME = 'File Management'




def getTeamData(team, sqlCon):
  """ """
  files = """ SELECT  file_map.alias as "file_code", file_map.disk_name as "file_name", file_map.file_type as "type"
                      FROM file_auth
                      INNER JOIN team_def ON team_def.team_id = file_auth.team_id
                      INNER JOIN file_map ON file_map.file_id = file_auth.file_id
                      WHERE team_def.team_name = '%s'
                      AND datetime('now') BETWEEN file_auth.stt_dt AND file_auth.end_dt
                      GROUP BY "team", "file_code", "file_name", "type" """ % team



  print(files)
  return sqlCon.select(files)

def getFilesPermissions(sqlCon, files, team):
  """ """
  fileDetails = """ SELECT file_map.disk_name, team_def.team_name, file_auth.temp_owner, file_auth.stt_dt, file_auth.end_dt
                  FROM file_map
                  INNER JOIN file_auth ON file_auth.file_id = file_map.file_id
                  LEFT OUTER JOIN team_def ON team_def.team_id = file_auth.team_id
                  WHERE file_map.disk_name in ('%s')""" % ("','".join(files))

  cache = {}
  for rec in sqlCon.select(fileDetails):
    print(rec)
    cache.setdefault(rec['disk_name'], []).append({'file': rec['disk_name'],'team': rec['team_name'], 'tmp_owner': rec['temp_owner'], 'stt_dt': rec['stt_dt'], 'end_dt': rec['end_dt']})

  return cache


def report(aresObj):
  """ """
  sqlCon = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  fileLst = []
  fileCache = {}
  summaryRecSet, chartRecSet = [], []
  for rec in getTeamData(aresObj.http['TEAM'], sqlCon):
    chartRecSet.append({'type': rec['type'], 'filename': rec['file_name'], 'file_code': rec['file_code']})
    fileLst.append(rec['file_name'])
    fileCache[rec['file_name']] = {'file_code': rec['file_code']}
  if not fileLst:
    aresObj.title('No Files allowed for your team !')
  else:
    fileDetails = getFilesPermissions(sqlCon, fileLst, aresObj.http['TEAM'])
    addFilePermission = aresObj.button('', cssCls=['fa fa-plus fa-5`x btn btn-link'])
    for file, details in fileDetails.items():
      nbFiles =  len(details)
      fileCache.update({'nbFiles': nbFiles, 'userDetails': details})
      addFilesModal = aresObj.modal(file, btnCls=['btn btn-link'])
      fileDetailsTable = aresObj.simpletable(fileDetails.get(file, [{'file': '' ,'team': '', 'tmp_owner': '', 'stt_dt': '', 'end_dt': ''}]),
                                                      [{'key': 'file', 'colName': 'File Name'},
                                                       {'key': 'team', 'colName': 'Team'},
                                                       {'key': 'tmp_owner', 'colName': 'Special User'},
                                                       {'key': 'stt_dt', 'colName': 'Start Date'},
                                                       {'key': 'end_dt', 'colName': 'End Date'},])
      aresObj.addTo(addFilesModal, addFilePermission)
      aresObj.addTo(addFilesModal, fileDetailsTable)
      summaryRecSet.append({'file': addFilesModal, 'nbFiles': nbFiles, 'userDetails': details})

    summaryTable = aresObj.simpletable(summaryRecSet, [{'key': 'file', 'colName': 'Files', 'type': 'object'},
                                                       {'key': 'nbFiles', 'colName': 'Nb Users'},
                                                       ])






  #
  # USE chartRecSet
  # pie = aresObj.pie(userRecSet, [{'key': 'user', 'colName': 'User'},
  #                               {'key': 'count', 'colName': 'Deployments done', 'type': 'number'}], headerBox='Deployers' )
  #
  # pie.setKeys(['user'])
  # pie.setVals(['count'])
  # aresObj.row([bar, pie])






