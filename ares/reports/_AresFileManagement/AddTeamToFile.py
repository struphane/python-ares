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

def getFileId(sqlCon, file):
  return sqlCon.select('''SELECT file_id FROM file_map WHERE disk_name = '%s' ''' % file)

def report(aresObj):
  """ """

  sqlCon = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  fileDetails = getFilesPermissions(sqlCon, aresObj.http['file'])
  import pprint
  # pprint.pprint(list(fileDetails))
  aresObj.title('File Detail for %s' % aresObj.http['file'])
  addFilePermission = aresObj.modal('', btnCls=['fa fa-plus fa-5x btn btn-link'])
  aresObj.simpletable(list(fileDetails), [{'key': 'disk_name', 'colName': 'File Name'},
                                                       {'key': 'team_name', 'colName': 'Team'},
                                                       {'key': 'temp_owner', 'colName': 'Special User'},
                                                       {'key': 'stt_dt', 'colName': 'Start Date'},
                                                       {'key': 'end_dt', 'colName': 'End Date'},])




  addButton = aresObj.button('Add')
  input = aresObj.input('Email address from Team to add')
  stt_dt = aresObj.date()
  end_dt = aresObj.date()

  col1 = aresObj.col([aresObj.text('Start Date'), stt_dt])
  col2 = aresObj.col([aresObj.text('End Date'), end_dt])
  row1 = aresObj.row([col1, col2])
  titleModal = aresObj.title('OR')
  input2 = aresObj.input('Special user to add (email address)')
  addButton2 = aresObj.button('Add')

  fileId = list(getFileId(sqlCon, aresObj.http['file']))[0]['file_id']

  addButton.clickWithValidCloseModal('addFilePermission', addFilePermission, {'team': input, 'type': 'team', 'file': fileId, 'stt_dt': stt_dt, 'end_dt': end_dt}, subPost=True)
  addButton2.clickWithValidCloseModal('addFilePermission', addFilePermission, {'user': input2, 'type': 'user', 'file': fileId, 'stt_dt': stt_dt, 'end_dt': end_dt}, subPost=True)

  aresObj.addTo(addFilePermission, row1)
  aresObj.addTo(addFilePermission, input)
  aresObj.addTo(addFilePermission, addButton)
  aresObj.addTo(addFilePermission, titleModal)
  aresObj.addTo(addFilePermission, input2)
  aresObj.addTo(addFilePermission, addButton2)



