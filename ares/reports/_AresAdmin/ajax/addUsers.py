from ares.Lib import AresSql


ADD_TEAM = """INSERT INTO team_def (team_id, team_name, role) VALUES (%s, '%s', '%s'); 
              INSERT INTO env_auth (env_id, team_id) 
              SELECT env_def.env_id, %s
              FROM env_def
              WHERE env_def.env_name = '%s';
                 """

ADD_BESPOKE_USER = """ INSERT INTO env_auth (temp_owner, team_id) 
                        SELECT '%s', team_id FROM team_def WHERE team_name = 'BESPOKE_TEAM'; """


def call(aresObj):

  map_role = {'Administrator': 'admin', 'User': 'role'}

  db = AresSql.SqliteDB(aresObj.http['REPORT_NAME'])
  if aresObj.http['type'] == 'bespoke':
    for user in aresObj.http['users'].split(','):
      db.modify(ADD_BESPOKE_USER % user.strip())
  else:
    team_map = {}
    for team in aresObj.http['team_dsc'].split(';'):
      team_name, team_email, team_id = team.split('#')
      team_map[team_email] = (team_id, team_name)

    current_team = aresObj.http['team[]']
    db.modify(ADD_TEAM % (team_map[current_team][0], team_map[current_team][1], map_role[aresObj.http['role']], team_map[current_team][0], aresObj.http['REPORT_NAME']))
  return "Addition completed"