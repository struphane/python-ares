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
  #aresObj.changeSiteColor('pink', 'yellow')
  aresObj.title("My report Title")
  # Example of DropDown selection
  #   - parameter 1: the title to be displayed in the object
  #   - parameter 2: the content of the dropdown (the items should be tuple (Name, hyperlink)
  dropdown = aresObj.dropdown('Portfolio', [('4', None), ('2', None), ('3', None), ('1', None)])
  dropdown.setDefault("2")


  # dropdown.targetScript('testService')
  # To disable some links
  dropdown.disable('link 1', None)
  # Because the hyperlink are not defined a click has to be defined to define the action

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

  data = [{"CCY": 'EUR', 'PRD': 'Bond', "PTF": '4', 'VAL': 66, 'VAL2': -1e4, 'COB': '2017-10-18'},
        {"CCY": 'EUR', 'PRD': 'Bond Option', "PTF": '4', 'VAL': 66, 'VAL2': -164, 'COB': '2017-10-17'},
        {"CCY": 'GBP', 'PRD': 'Bond', "PTF": '2', 'VAL': 45, 'VAL2': 3, 'COB': '2017-10-15'},
        {"CCY": 'USD', 'PRD': 'Cds', "PTF": '4', 'VAL': 103, 'VAL2': 100, 'COB': '2017-10-20'},
        {"CCY": 'USD', 'PRD': 'Cds', "PTF": '4', 'VAL': 103, 'VAL2': 100, 'COB': '2017-10-19'},
        {"CCY": 'GBP', 'PRD': 'Bond', "PTF": '2', 'VAL': 43, 'VAL2': 3, 'COB': '2017-10-21'},
        {"CCY": 'GBP', 'PRD': 'Bond', "PTF": '3', 'VAL': 26, 'VAL2': 36, 'COB': '2017-10-19'},
        {"CCY": 'AUD', 'PRD': 'Cds', "PTF": '4', 'VAL': 67, 'VAL2': -34, 'COB': '2017-10-21'},
        {"CCY": 'GBP', 'PRD': 'Bond', "PTF": '4', 'VAL': 66, 'VAL2': -1344, 'COB': '2017-10-22'},
        {"CCY": 'GBP', 'PRD': 'Bond', "PTF": '4', 'VAL': 60, 'VAL2': -144, 'COB': '2017-10-23'},
        {"CCY": 'GBP', 'PRD': 'Cds', "PTF": '4', 'VAL': 20, 'VAL2': -1e4, 'COB': '2017-10-18'},
        {"CCY": 'GBP', 'PRD': 'Bond', "PTF": '4', 'VAL': 36, 'VAL2': -164, 'COB': '2017-10-17'}]

  header = [
    {'key': "CCY", 'colName': 'Currency'},
    {'key': "COB", 'colName': 'Close of business'},
    {'key': "PRD", 'colName': 'Product'},
    {'key': "PTF", 'colName': 'Portfolio'},
    {'key': "VAL", 'colName': 'Notional'},
    {'key': "VAL2", 'colName': 'Pv'}
  ]

  # dropdownPrd = aresObj.select(data, 'PRD')
  # dropdownPrd.setDefault("Cds")
  #
  # pie = aresObj.spider(data, header, headerBox='Currencies')
  # pie.setSeries(['CCY'])
  # pie.setY(['VAL2'])
  # pie.setX('PRD')
  #pie.filterSerie('USD')
  #pie.setExtVals(['PTF', 'PRD'], [dropdown, dropdownPrd])

  # bar = aresObj.wordcloud(data, header, headerBox='Currencies')
  # bar.setKeys(['CCY', 'COB'])
  # bar.setVals(['VAL'])
  # bar.setExtVals(['PTF', 'PRD'], [dropdown, dropdownPrd])
  #
  # aresObj.row([pie, bar])

  table = aresObj.table(data, header)
  #table.hideColumns([0, 1])
  table.pivot(['CCY', 'PTF', 'COB'], ['VAL2'])
  table.callBackFooterColumns()
        #{ 'visible': False, 'targets': [1,3] }

  #table = aresObj.simpletable(data, header, headerBox='Currencies', cssCls=['table'])
  #table.pivot(['CCY', 'PTF', 'COB'], ['VAL2'], filters={'PTF': ['1']})
  #table.cssRowMouseHover()