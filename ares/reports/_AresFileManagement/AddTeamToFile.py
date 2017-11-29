"""

"""

from ares.Lib import AresSql
from Libs import mailer


NAME = 'Add Permission'

def getFilesPermissions(sqlCon, file):
  """ """
  fileDetails = """ SELECT file_map.disk_name, team_def.team_name, file_auth.temp_owner, file_auth.stt_dt, file_auth.end_dt
                  FROM file_map
                  INNER JOIN file_auth ON file_auth.file_id = file_map.file_id
                  LEFT OUTER JOIN team_def ON team_def.team_id = file_auth.team_id
                  WHERE file_map.disk_name = '%s'""" % file

  return sqlCon.select(fileDetails)

def report(aresObj):
  """ """

  sqlCon = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  fileDetails = getFilesPermissions(sqlCon, aresObj.http['file'])
  aresObj.title('File Detail for %s' % aresObj.http['file'])
  addFilePermission = aresObj.modal('', btnCls=['fa fa-plus fa-5x btn btn-link'])
  aresObj.simpletable(list(fileDetails), [{'key': 'disk_name', 'colName': 'File Name'},
                                                       {'key': 'team_name', 'colName': 'Team'},
                                                       {'key': 'temp_owner', 'colName': 'Special User'},
                                                       {'key': 'stt_dt', 'colName': 'Start Date'},
                                                       {'key': 'end_dt', 'colName': 'End Date'},])




  addButton = aresObj.button('Add')
  input = aresObj.input('Team to add')
  teamRow = aresObj.row([input, addButton])
  input2 = aresObj.input('Special user to add')
  addButton2 = aresObj.button('Add')
  userRow = aresObj.row([input2, addButton2])

  addButton.clickWithValidCloseModal('addFilePermission', addFilePermission, {'team': input, 'type': 'team'}, subPost=True)
  addButton2.clickWithValidCloseModal('addFilePermission', addFilePermission, {'user': input2, 'type': 'user'}, subPost=True)


  aresObj.addTo(addFilePermission, teamRow)
  aresObj.addTo(addFilePermission, userRow)





  #
  # USE chartRecSet
  # pie = aresObj.pie(userRecSet, [{'key': 'user', 'colName': 'User'},
  #                               {'key': 'count', 'colName': 'Deployments done', 'type': 'number'}], headerBox='Deployers' )
  #
  # pie.setKeys(['user'])
  # pie.setVals(['count'])
  # aresObj.row([bar, pie])






