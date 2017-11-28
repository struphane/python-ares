"""

"""

from ares.Lib import AresSql
from Libs import mailer


NAME = 'Add Permission'


def report(aresObj):
  """ """
  sqlCon = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  for rec in getTeamData(aresObj.http['TEAM'], sqlCon):
    chartRecSet.append({'type': rec['type'], 'filename': rec['file_name'], 'file_code': rec['file_code']})
    fileLst.append(rec['file_name'])
    fileCache[rec['file_name']] = {'file_code': rec['file_code']}
  if not fileLst:
    aresObj.title('No Files allowed for your team !')
  else:
    fileDetails = getFilesPermissions(sqlCon, fileLst, aresObj.http['TEAM'])
    addFilePermission = aresObj.modal('', cssCls=['fa fa-plus fa-5x btn btn-link'])
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
      summaryRecSet.append({'file': aresObj.internalLink(file, ), 'nbFiles': nbFiles, 'userDetails': details})

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






