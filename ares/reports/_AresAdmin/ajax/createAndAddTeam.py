from ares.Lib import AresSql
from flask import url_for
from pprint import pprint

def call(aresObj):
  return url_for('ares.createTeam', team=aresObj.http['team_name'], team_email=aresObj.http['team_email'], role=aresObj.http['role'], report_name=aresObj.http['REPORT_NAME'])