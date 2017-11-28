INSERT INTO logs_download (email, team_name, env_id)
SELECT '%(email)s', '%(team)s', env_def.env_id FROM env_def WHERE env_def.env_name = '%(report_name)s'