from ares.Lib import AresSql


ADD_TEAM = """ INSERT INTO env_auth (team_id, role)
                        SELECT team_id, '%s' FROM team_def WHERE team_name = '%s'"""

ADD_BESPOKE_USER = """ INSERT INTO env_auth (temp_owner, team_id) 
                        SELECT '%s', team_id FROM team_def WHERE team_name = 'BESPOKE_TEAM'"""

def call(aresObj):
  if aresObj.http['type'] == 'bespoke':
    for user in aresObj.http['users'].split(','):
      db = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
      db.modify(ADD_BESPOKE_USER % user.strip())
  else:
    db = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
    db.modify(ADD_BESPOKE_USER % (aresObj.http['role'], aresObj.http['team']))
  return "Addition completed"