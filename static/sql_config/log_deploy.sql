INSERT INTO logs_deploy (uid, folder, file, type)
SELECT  user_accnt.uid, "%(report_name)s", "%(file)s", "%(type)s"
FROM user_accnt
WHERE user_accnt.email_addr = '%(usr_id)s';