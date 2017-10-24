

def report(aresObj):
  """  """
  aresObj.title2("How to create a MultiBar Chart")
  aresObj.preformat(
    '''
      [{"CCY": 'EUR', "PTF": '123', 'VAL': 13, 'VAL2': -43, 'COB': '2017-10-18'},
       {"CCY": 'EUR', "PTF": '124', 'VAL': 64, 'VAL2': -34, 'COB': '2017-10-18'},
       {"CCY": 'GBP', "PTF": '34', 'VAL': 72, 'VAL2': -64, 'COB': '2017-10-18'},
       {"CCY": 'USD', "PTF": '74', 'VAL': 25, 'VAL2': -13, 'COB': '2017-10-18'}]
    '''
  )
  recordSet = [{"CCY": 'EUR', "PTF": '123', 'VAL': 13, 'VAL2': -43, 'COB': '2017-10-18'},
               {"CCY": 'EUR', "PTF": '124', 'VAL': 64, 'VAL2': -34, 'COB': '2017-10-18'},
               {"CCY": 'GBP', "PTF": '34', 'VAL': 72, 'VAL2': -64, 'COB': '2017-10-18'},
               {"CCY": 'USD', "PTF": '74', 'VAL': 25, 'VAL2': -13, 'COB': '2017-10-18'}]

  header = [{'key': 'CCY', 'colName': 'Currency'},
            {'key': 'PTF', 'colName': 'Portfolio'},
            {'key': 'VAL', 'colName': 'Value'},
            {'key': 'VAL2', 'colName': 'Value 2'},
            {'key': 'COB', 'colName': 'Close of Business'}]

  aresObj.title4("Display a 2D donut chart with multiple keys and values")
  multiBar = aresObj.multiBar(recordSet, header)
  multiBar.setSeries(['CCY', "PTF"])
  multiBar.setX('COB') #
  multiBar.setY(['VAL', 'VAL2'])

  aresObj.title4("Display a 2D donut chart with multiple keys and values")
  horizBar = aresObj.horizBar(recordSet, header)
  horizBar.setSeries(['CCY', "PTF"])
  horizBar.setX('COB') #
  horizBar.setY(['VAL', 'VAL2'])
