"""

"""

from ares.Lib import AresSql
from Libs import mailer


NAME = 'Administration'




def getTeamData(aresObj, sqlCon):
  """ """
  nbGlobalUsers = """ SELECT team_def.team_name as "team", team_def.role as "role"
                      FROM env_auth 
                      INNER JOIN env_def ON env_def.env_id = env_auth.env_id 
                      INNER JOIN team_def ON team_def.team_id = env_auth.team_id
                      WHERE  env_def.env_name = '%s'
                      AND datetime('now') BETWEEN env_auth.stt_dt AND env_auth.end_dt
                      GROUP BY "role" """ % aresObj.http['REPORT_NAME']


  return sqlCon.select(nbGlobalUsers)

def getTempAdminUsers(aresObj, sqlCon):
  """ """
  nbBespokeUsers = """ SELECT env_auth.temp_owner as "user", 'Normal' as "role"
                       FROM env_auth
                       INNER JOIN env_def ON env_def.env_id = env_auth.env_id
                       WHERE env_def.env_name = '%s'""" % aresObj.http['REPORT_NAME']

  return sqlCon.select(nbBespokeUsers)


def getDeployData(aresObj, sqlCon):
  """ """
  deploy_logs = """ SELECT email as "user"
                    ,strftime('%%Y-%%m-%%d', lst_mod_dt) as "date"
                    ,count(*) as "count"
                    FROM logs_deploy
                    WHERE folder = '%s' 
                    GROUP by "date" """ % aresObj.http['REPORT_NAME']

  return sqlCon.select(deploy_logs)

def getAuthorizedUsers(aresObj, sqlCon):
  """ """
  auth_users = """ SELECT 
                  team_def.team_name as "team" 
                  ,role
                  FROM team_def
                  INNER JOIN env_auth ON env_auth.team_id = team_def.team_id
                  INNER JOIN env_def ON env_def.env_id = env_auth.env_id
                  WHERE env_def.env_name = '%s' """ % aresObj.http['REPORT_NAME']

  return sqlCon.select(auth_users)



def ajaxCall(aresObj, userLst):
  """ Pass in the list of user from the input zone
   REMOVE FOR LATER : ARES mail details
   address: ares.pymailer@gmail.com
   password: H3reCom3sAReS

   """
  mailer._DEBUG = False
  mail_server = mailer.SMTPServer('smtp.gmail.com', 587)
  mail_server.connect(user='ares.pymailer@gmail.com', password='H3reCom3sAReS')
  ADD_USER = """ INSERT INTO team_def (team_name) VALUES ('%s');"""
  ADD_AUTH = """ INSERT INTO env_auth (env_id, team_id) VALUES (%s, %s);"""
  sqlCon = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])

  env_id = list(sqlCon.select("SELECT env_id FROM env_def WHERE env_name = '%s'" % aresObj.http['REPORT_NAME']))[0]['env_id']

  authRecSet = [rec['user'] for rec in list(getAuthorizedUsers(aresObj, sqlCon))]
  mail_subject = 'You have been authorized to a new environment in AReS'
  mail_content = """Hello,\nYou are now allowed to view the content of the report %s.\nSimply connect to the application using your personal token: %s\nSee you soon !\nAReS Team """
  for user in userLst:
    if user not in authRecSet:
      _, add_token = createUserAccnt(user)
      #add new user into user_accnt
      sqlCon.modify(ADD_USER % (user, add_token))
      uid = list(sqlCon.select('select last_insert_rowid() as "uid";'))[0]['uid']
      #add entry into env_auth
      sqlCon.modify(ADD_AUTH % (env_id, uid))
      email = mailer.Email('ares.pymailer@gmail.com', [user], mail_subject, mail_content % (aresObj.http['REPORT_NAME'], add_token))
      mail_server.sendmail(email)


def report(aresObj):
  # userRecordSet = getEnvData(aresObj)
  sqlCon = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  nbUsers, nbTeams, nbBespoke = 0, 0, 0
  table2Rec = []
  for rec in getTeamData(aresObj, sqlCon):
    nbUsers += 1
    nbTeams += 1
    radiobutton = aresObj.radio([{'role': 'admin'}, {'role': 'user'}], 'role', [{'key': 'role', 'colName': 'Role'}])
    radiobutton.select(rec['role'])
    radiobutton.clickWithPost('changePermissions', {'team': rec['team']})
    table2Rec.append({'user': rec['team'], 'role': radiobutton})

  for rec in getTempAdminUsers(aresObj, sqlCon):
    nbUsers += 1
    nbBespoke += 1
    table2Rec.append({'user': rec['user'], 'role': rec['role']})

  deployRec = list(getDeployData(aresObj, sqlCon))

  aresObj.title("Env Administration - %s" % aresObj.http['REPORT_NAME'])
  aresObj.newline()
  aresObj.newline()
  tableRec = [{'total': str(nbUsers), 'Teams': str(nbTeams), 'Bespoke Users': str(nbBespoke)}]
  aresObj.simpletable(tableRec, [{'key': 'total', 'colName': 'Total Users'},
                                         {'key': 'Teams', 'colName': 'Teams'},
                                         {'key': 'Bespoke Users', 'colName': 'Bespoke Users'}])
  aresObj.newline()
  aresObj.newline()

  input =aresObj.input(value='Authorise bespokes users to view this report (comma separated list)')
  submitButton = aresObj.button('Submit')
  submitButton.clickWithValid('addUsers', {'users': input, 'type': 'bespoke'})
  col1 = aresObj.col([input, submitButton])

  input2 =aresObj.input(value='Allow new teams to view/edit this report')
  btnText = aresObj.text('Choose permission:')
  roleButton = aresObj.radio([{'role': 'admin'}, {'role': 'user'}], 'role', [{'key': 'role', 'colName': 'Role'}])
  col2 = aresObj.col([btnText, aresObj.newline(), roleButton])
  roleRow = aresObj.row([input2, col2])
  submitButton2 = aresObj.button('Submit')
  submitButton2.clickWithValid('addUsers', {'team': input2, 'role': roleButton, 'type': 'team'})
  col3 = aresObj.col([roleRow, submitButton2])



  aresObj.row([col1, col3])

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

  pie = aresObj.pie(userRecSet, [{'key': 'user', 'colName': 'User'},
                                {'key': 'count', 'colName': 'Deployments done', 'type': 'number'}], headerBox='Deployers' )

  pie.setKeys(['user'])
  pie.setVals(['count'])
  aresObj.row([bar, pie])






