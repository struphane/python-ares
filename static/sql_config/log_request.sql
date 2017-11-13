INSERT INTO logs_con (email, team_name env_id, script)
SELECT "%(username)s", "%(team_name)s", env_def.env_id, '%(script_name)s'
FROM env_def
WHERE env_def.env_name = '%(env_name)s';