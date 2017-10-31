INSERT INTO file_map (alias, file_type, disk_name) VALUES ('%(filename)s', '%(file_type)s', '%(filename)s');
INSERT INTO file_auth (file_id, uid)
SELECT file_map.file_id, user_accnt.uid
FROM file_map, user_accnt
WHERE file_map.disk_name = '%(filename)s' and user_accnt.email_addr = '%(usr_id)s';