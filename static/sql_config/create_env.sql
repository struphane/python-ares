INSERT INTO team_def (team_name, role) VALUES ('%(team_name)s', 'admin');
INSERT INTO env_def (env_name) VALUES ('%(env_name)s');
INSERT INTO env_auth (env_id, team_id)
SELECT env_def.env_id, team_def.team_id
FROM env_def, team_def
WHERE env_def.env_name = '%(env_name)s' and team_def.team_name = '%(team_name)s';