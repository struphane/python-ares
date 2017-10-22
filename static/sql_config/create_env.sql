INSERT INTO user_accnt (email_addr, role, hash_id) VALUES ('%(usr_id)s', 'admin', '%(hash_id)s');
INSERT INTO env_def (env_name) VALUES ('%(env_name)s');
INSERT INTO env_auth (env_id, uid)
SELECT env_def.env_id, user_accnt.uid
FROM env_def, user_accnt
WHERE env_def.env_name = '%(env_name)s' and user_accnt.email_addr = '%(usr_id)s';