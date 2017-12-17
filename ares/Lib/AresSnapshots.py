from selenium import webdriver
# from flask import url_for
import os
from future.standard_library import install_aliases
install_aliases()
# from flask import current_app
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

driverMap = {'CHROME': webdriver.Chrome, 'EXPLORER': webdriver.Ie, 'FIREFOX': webdriver.Firefox}

authenticationParams = {'email_addr': 'ares@ares.com', 'password': 'admin'}

def passAuthentication():
  data = urlencode(authenticationParams).encode('utf-8')
  print(data)
  req = Request(r'http://127.0.0.1:5000/reports/ares/login', data=data)
  print(req)
  response = urlopen(req)
  print(response.read())

def takeSnapshot(report_name, script_name=None, driver='CHROME', *args, **kwargs):
  """ """
  tempDir = r'C:\Users\Tinels972\PycharmProjects\python-ares'
  # snapDir = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'snapshot')
  # driver = driverMap.get(driver.upper(), webdriver.Chrome)(os.path.join(current_app.config['ROOT_PATH'], 'system', 'webDrivers'))
  driver = driverMap.get(driver.upper(), webdriver.Chrome)(os.path.join(tempDir, 'system', 'webDrivers', 'chromedriver'))
  if not script_name:
    script_name = report_name
  # url = url_for('ares.run_report', report_name=report_name, script_name=script_name, **kwargs)
  url = r'http://"nelson.allain@gmail.com:blabla"@127.0.0.1:5000/reports/index'
  driver.get(url)
  # driver.save_screenshot(os.path.join(snapDir, report_name, '_', script_name, '.png'))
  driver.save_screenshot(os.path.join(tempDir, 'snapshot_test.png'))
  driver.quit()


def takeSnapshotTest(report_name, script_name=None, driver='CHROME', *args, **kwargs):
  """ """
  tempDir = r'C:\Users\Tinels972\PycharmProjects\python-ares'
  # snapDir = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'snapshot')
  # driver = driverMap.get(driver.upper(), webdriver.Chrome)(os.path.join(current_app.config['ROOT_PATH'], 'system', 'webDrivers'))
  driver = driverMap.get(driver.upper(), webdriver.Chrome)(os.path.join(tempDir, 'system', 'webDrivers', 'chromedriver'))
  if not script_name:
    script_name = report_name
  # url = url_for('ares.run_report', report_name=report_name, script_name=script_name, **kwargs)
  url = r'http://"nelson.allain@gmail.com:blabla"@127.0.0.1:5000/reports/index'
  driver.get(url)
  # driver.save_screenshot(os.path.join(snapDir, report_name, '_', script_name, '.png'))
  driver.save_screenshot(os.path.join(tempDir, 'snapshot_test.png'))
  driver.quit()


passAuthentication()
print('toto')
# takeSnapshotTest('')