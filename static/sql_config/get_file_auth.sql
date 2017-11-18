SELECT fm.alias, fm.disk_name
FROM file_map fm
INNER JOIN file_auth fa ON fa.file_id = fm.file_id
INNER JOIN team_def td ON td.team_id = fa.team_id
WHERE td.team_name = '%(team)s'
AND fm.alias = '%(file_cod)s'
