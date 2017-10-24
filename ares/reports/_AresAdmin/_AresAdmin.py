"""

"""

from ares.Lib import AresSql
NAME = 'Administrator'



def getUserData(aresObj, sqlCon):
  """ """
  nbGlobalUsers = """ SELECT user_accnt.email_addr as "user", user_accnt.role as "role"
                      FROM env_auth 
                      INNER JOIN env_def ON env_def.env_id = env_auth.env_id 
                      INNER JOIN user_accnt ON user_accnt.uid = env_auth.uid
                      WHERE  env_def.env_name = '%s'
                      AND date('now') BETWEEN env_auth.stt_dt AND env_auth.end_dt
                      GROUP BY "role" """ % aresObj.http['REPORT_NAME']

  return sqlCon.select(nbGlobalUsers)

def getDeployData(aresObj, sqlCon):
  """ """
  deploy_logs = """ SELECT user_accnt.email_addr as "user"
                    ,strftime('%%Y-%%m-%%d', lst_mod_dt) as "date"
                    ,count(*) as "count"
                    FROM logs_deploy
                    INNER JOIN user_accnt ON user_accnt.uid = logs_deploy.uid
                    WHERE folder = '%s' 
                    GROUP by "date" """ % aresObj.http['REPORT_NAME']

  return sqlCon.select(deploy_logs)


def report(aresObj):
  # userRecordSet = getEnvData(aresObj)
  sqlCon = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  nbUsers, ndAdmin, nbWatchers = 0, 0, 0
  table2Rec = []
  for rec in getUserData(aresObj, sqlCon):
    nbUsers += 1
    ndAdmin += 1 if rec['role'] == 'admin' else 0
    nbWatchers += 1 if rec['role'] != 'admin' else 0
    radiobutton = aresObj.radio([{'role': 'admin'}, {'role': 'user'}], 'role', [{'key': 'role', 'colName': 'Role'}])
    radiobutton.select(rec['role'])
    table2Rec.append({'user': rec['user'], 'role': radiobutton})

  deployRec = list(getDeployData(aresObj, sqlCon))

  aresObj.title("Env Administration - %s" % aresObj.http['REPORT_NAME'])
  aresObj.newline()
  aresObj.newline()
  tableRec = [{'total': str(nbUsers), 'admin': str(ndAdmin), 'watchers': str(nbWatchers)}]
  aresObj.simpletable(tableRec, [{'key': 'total', 'colName': 'Total Users'},
                                         {'key': 'admin', 'colName': 'Contributors'},
                                         {'key': 'watchers', 'colName': 'Watchers'}])
  aresObj.newline()
  aresObj.newline()

  input =aresObj.input(value='Authorise users to view this report (comma separated list)')
  submitButton = aresObj.button('Submit')
  aresObj.col([input, submitButton])

  aresObj.newline()
  aresObj.newline()
  aresObj.simpletable(table2Rec, [{'key': 'user', 'colName': 'User'},
                                  {'key': 'role', 'colName': 'Role', 'type': 'object'}])
  aresObj.newline()
  aresObj.newline()
  bar = aresObj.bar(deployRec, [{'key': 'date', 'colName': 'Date'},
                                {'key': 'count', 'colName': 'Deployments', 'type': 'number'}], headerBox='Deployments' )

  bar.setKeys(['date'])
  bar.setVals(['count'])

  userRecSet = []
  userDeployRec = {}
  for rec in deployRec:
    if rec['user'] not in userDeployRec:
      userDeployRec[rec['user']] = 1
    else:
      userDeployRec[rec['user']] += 1

  for user, count in userDeployRec.items():
    userRecSet.append({'user': user, 'count': count})

  print(userRecSet)
  pie = aresObj.pie(userRecSet, [{'key': 'user', 'colName': 'User'},
                                {'key': 'count', 'colName': 'Deployments done', 'type': 'number'}], headerBox='Deployers' )

  pie.setKeys(['user'])
  pie.setVals(['count'])
  aresObj.row([bar, pie])






