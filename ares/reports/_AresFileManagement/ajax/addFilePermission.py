from flask import request, url_for
from ares.Lib import AresSql

def call(aresObj):
  """ TODO: Add call in report.py to add teams in master db and then in env db """
  if aresObj.http['type'] == 'team':
    return url_for('ares.addFileAuth', report_name=aresObj.http['REPORT_NAME'], team=aresObj.http['team'], file_id=aresObj.http['file'], stt_dt=aresObj.http['stt_dt'], end_dt=aresObj.http['end_dt'])

  return url_for('ares.addFileAuth', report_name=aresObj.http['REPORT_NAME'], temp_owner=aresObj.http['user'], file_id=aresObj.http['file'], stt_dt=aresObj.http['stt_dt'], end_dt=aresObj.http['end_dt'])


