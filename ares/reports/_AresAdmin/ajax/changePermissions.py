from ares.Lib import AresSql


UPDATE_PERMISSION = """ UPDATE team_def
                        SET role = '%s' 
                        WHERE team_name = '%s' """

def call(aresObj):
  db = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  role = 'Normal' if aresObj.http['btnValue'] == 'user' else 'admin'
  db.modify(UPDATE_PERMISSION % (role, aresObj.http['team']))
  return "Role Updated"