INSERT INTO logs_con (uid, env_id, script)
SELECT user_accnt.uid, env_def.env_id, '%(script_name)s'
FROM env_def, user_accnt
WHERE env_def.env_name = '%(env_name)s' and user_accnt.email_addr = '%(usr_id)s';