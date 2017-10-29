""" [SCRIPT COMMENT]

>>>> Important variables / functions

In the python layer
    aresObj.http['FILE'] is the current file
    aresObj.http['REPORT_NAME'] is the current report environment name
    aresObj.http['DIRECTORY'] is the report location

     def readFile(self, file, subfolders=None):
     def createFile(self, file, subfolders=None, checkFileExist=True):
     def getFolders(self):
     def getFiles(self, subfolders):


In the javascript layer
    display(data) to return the result in a notification modal popup
    preloader() to show a loading page

"""


NAME = 'Olivier' # The Report Name in the left menu
# The Shortcuts should be defined as below
# [(Cateogry Name, [List of the script in the root directory])]
# It is only possible to create new links for scripts in the root
SHORTCUTS = [] # All the possible link to other pages

import random

def report(aresObj):
  '''
  Write your function below
  '''
  aresObj.title("My report Title")
  # Example of DropDown selection
  #   - parameter 1: the title to be displayed in the object
  #   - parameter 2: the content of the dropdown (the items should be tuple (Name, hyperlink)
  dropdown = aresObj.ajaxDropdown('Test', [('link 1', None),
                                       ('Other', [('link 2', None),
                                                 ('link 3', [('link 4', None)] )])
                                                 ])
  dropdown.targetScript('testService')
  # To disable some links
  dropdown.disable('link 1', None)
  # Because the hyperlink are not defined a click has to be defined to define the action

  # Example of a Radio select HTML object
  #   - parameter 1: the key in the recordSet to be used to define the range of values
  #   - parameter 2: the recordset (a list of dictionaries)
  #   - parameter 3: the header definition of the recordset
  radio = aresObj.radio([{'CCY': 'EUR'}, {'CCY': 'HUF'}, {'CCY': 'USD'}], 'CCY',
                        [{'key': 'CCY', 'colName': 'Currency'}])

  radio.select('EUR')
  radio.jsFnc('alert(%s)' % radio.val)

  # Example of a pie chart
  ccys = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF']
         #'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC',
         #'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP',
         #'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS',
         #'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW',
         #'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT',
         #'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR',
         #'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR',
         #'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SPL*', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT',
         #'TND', 'TOP', 'TRY', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 'VUV',
         #'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWD']

  data = []
  size = len(ccys)
  for i in range(1000):
    val = random.randrange(0, 1000)
    mod = val % size
    data.append({"CCY": ccys[mod], 'VAL': val, 'COB': '2017-10-20'})

  header = [
    {'key': "CCY", 'colName': 'Currency'},
    {'key': "VAL", 'colName': 'Value'}
  ]

  pie = aresObj.pie(data, header, headerBox='Currencies')
  pie.setKeys(['CCY'])
  pie.setVals(['VAL'])

  dropdown.click([pie])

  data = [{"CCY": 'EUR', "PTF": '4', 'VAL': 66, 'VAL2': -1e4, 'COB': '2017-10-18'},
        {"CCY": 'EUR', "PTF": '4', 'VAL': 66, 'VAL2': -164, 'COB': '2017-10-17'},
        {"CCY": 'GBP', "PTF": '2', 'VAL': 45, 'VAL2': 3, 'COB': '2017-10-15'},
        {"CCY": 'GBP', "PTF": '1', 'VAL': 103, 'VAL2': 100, 'COB': '2017-10-20'},
        {"CCY": 'GBP', "PTF": '2', 'VAL': 43, 'VAL2': 3, 'COB': '2017-10-21'},
        {"CCY": 'GBP', "PTF": '3', 'VAL': 26, 'VAL2': 36, 'COB': '2017-10-19'},
        {"CCY": 'GBP', "PTF": '4', 'VAL': 67, 'VAL2': -34, 'COB': '2017-10-21'},
        {"CCY": 'GBP', "PTF": '4', 'VAL': 66, 'VAL2': -1344, 'COB': '2017-10-22'},
        {"CCY": 'GBP', "PTF": '4', 'VAL': 60, 'VAL2': -144, 'COB': '2017-10-23'},
        {"CCY": 'GBP', "PTF": '4', 'VAL': 20, 'VAL2': -1e4, 'COB': '2017-10-18'},
        {"CCY": 'GBP', "PTF": '4', 'VAL': 36, 'VAL2': -164, 'COB': '2017-10-17'}]

  header = [
    {'key': "CCY", 'colName': 'Currency', 'color': 'pink', 'barStyle': True},
    {'key': "PTF", 'colName': 'Portfolio'},
    {'key': "COB", 'colName': 'Close of Business', 'type': '%Y-%m-%d'},
    {'key': "VAL", 'colName': 'Value'},
    {'key': "VAL2", 'colName': 'Value 2'}
  ]

  table = aresObj.simpletable(data, header, headerBox='Currencies', cssCls=['table'])
  table.pivot(['CCY', 'PTF', 'COB'], ['VAL2'])
  table.cssRowMouseHover()