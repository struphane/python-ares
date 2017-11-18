SELECT fm.alias, fm.disk_name
FROM file_map fm
WHERE fm.file_type = '%(type)s'
AND fm.alias = '%(file_cod)s'
