

def report(aresObj):
  """

  """
  aresObj.title2("How to create a Pie Chart")

  aresObj.title4("Everything starts with the data")
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

  aresObj.preformat(
    '''
      [{'key': 'CCY', 'colName': 'Currency'},
      {'key': 'PTF', 'colName': 'Portfolio'},
      {'key': 'VAL', 'colName': 'Value'},
      {'key': 'VAL2', 'colName': 'Value 2'},
      {'key': 'COB', 'colName': 'Close of Business'}]
    '''
  )

  header = [{'key': 'CCY', 'colName': 'Currency'},
            {'key': 'PTF', 'colName': 'Portfolio'},
            {'key': 'VAL', 'colName': 'Value'},
            {'key': 'VAL2', 'colName': 'Value 2'},
            {'key': 'COB', 'colName': 'Close of Business'}]

  aresObj.title4("Display a 2D pie chart")
  pie = aresObj.pie(recordSet, header)
  pie.setKeys(["CCY"])
  pie.setVals(["VAL"])
  aresObj.row([
    aresObj.preformat('''
    pie = aresObj.pie(recordSet, header)
    pie.setKeys(["CCY"])
    pie.setVals(["VAL"])
                      '''), pie])

  aresObj.title4("Display a 2D pie chart with multiple keys")
  pie1 = aresObj.pie(recordSet, header)
  pie1.setKeys(["CCY", 'PTF'])
  pie1.setVals(["VAL"])
  aresObj.row([
    aresObj.preformat('''
      pie = aresObj.pie(recordSet, header)
      pie.setKeys(["CCY", 'PTF'])
      pie.setVals(["VAL"])
                      '''), pie1])

  aresObj.title4("Display a 2D pie chart with multiple keys and values")
  pie2 = aresObj.pie(recordSet, header)
  pie2.setKeys(["CCY", 'PTF'], selected=1)
  pie2.setVals(["VAL", 'VAL2'])
  aresObj.row([
    aresObj.preformat('''
    pie = aresObj.pie(recordSet, header)
    pie.setKeys(["CCY", 'PTF'], selected=1)
    pie.setVals(["VAL", 'VAL2'])
                      '''), pie2])


  aresObj.internalLink("Next training", 'AresExChartDonut')