REPLACE INTO file_map (alias, file_type, disk_name) VALUES ('%(fileCode)s', '%(file_type)s', '%(filename)s');
INSERT INTO file_auth (file_id, team_id)
SELECT file_map.file_id, team_def.team_id
FROM file_map, team_def
WHERE file_map.disk_name = '%(filename)s' and team_def.team_name = '%(team_name)s';