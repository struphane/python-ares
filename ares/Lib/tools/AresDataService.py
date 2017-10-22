""" Pivot Data Service

"""

from __future__ import print_function

# For Python 2.7
# you need to have request installed on your computer
# pip install requests

#Ares documentation is available here:
#  http://127.0.0.1:5000/reports/doc
#[This documentation is autogenerated from the script comments]

from __future__ import print_function
import requests
import json
import AresInstall # This import will work locally (because the structure is a bit different)

postUrlPivtoService = AresInstall.SERVER_PATH + r'/reports/pivotData/%s'

if __name__ == '__main__':
  """
  This will return the data that the service will produce.
  You can use this service locally or in your ajax service to convert the recordSet directly in the correct format
  for your chart.

  The update function in the different chart will use this service in order to change the recordSet and then
  update the chart. So you can test it locally by first using the python module locally then by using this Ares
  wrapper service
  """
  chart = 'pie' # The name should be the alias of the chart you want to test
  # Example of recordSet
  data = [{"CCY": 'GBP', 'VAL': 100, 'COB': '2017-10-20'},
        {"CCY": 'GBP', 'VAL': 40, 'COB': '2017-10-21'},
        {"CCY": 'EUR', 'VAL': 23, 'COB': '2017-10-19'},
        {"CCY": 'USD', 'VAL': 66, 'COB': '2017-10-21'}]
  reponse = requests.post(postUrlPivtoService % chart,
                          data=json.dumps({'RECORDSET': data, 'KEY': 'COB', 'VAL': 'VAL'}),
                          headers={'content-type': 'application/json'})
  # This example for this kind of 2D chart will return
  # [["2017-10-21", 106.0], ["2017-10-20", 100.0], ["2017-10-19", 23.0]]
  print (json.loads(reponse.text))