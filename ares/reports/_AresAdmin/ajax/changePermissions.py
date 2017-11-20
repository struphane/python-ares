from ares.Lib import AresSql


UPDATE_PERMISSION = """ UPDATE team_def
                        SET role = '%s' 
                        WHERE team_name = '%s' """

def call(aresObj):
  db = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  db.modify(UPDATE_PERMISSION % (aresObj.http['btnValue'], aresObj.http['team']))
  return "Role Updated"