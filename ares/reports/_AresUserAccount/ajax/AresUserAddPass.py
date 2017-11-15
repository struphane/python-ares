from flask import url_for

def call(aresObj):
  sourcename = aresObj.http['source']
  src_username = aresObj.http['username']
  src_pwd = aresObj.http['pwd']
  return url_for('ares.createDataSource', source=sourcename, app_id=aresObj.http['app_id'], username=src_username, password=src_pwd)
