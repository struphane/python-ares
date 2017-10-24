

def report(aresObj):
  """

  """
  aresObj.title2("How to create a Donut Chart")

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

  aresObj.title4("Display a 2D donut chart with multiple keys and values")
  donut = aresObj.donut(recordSet, header)
  donut.setKeys(["CCY", 'PTF'], selected=1)
  donut.setVals(["VAL", 'VAL2'])
  aresObj.row([
    aresObj.preformat('''
    donut = aresObj.donut(recordSet, header)
    donut.setKeys(["CCY", 'PTF'], selected=1)
    donut.setVals(["VAL", 'VAL2'])
                      '''), donut])


  aresObj.title4("How to customize your chart")
  donut1 = aresObj.donut(recordSet, header)
  donut1.addChartAttr({'startAngle': "function(d) { return d.startAngle/2 -Math.PI/2 }"})
  donut1.addChartAttr({'endAngle': "function(d) { return d.endAngle/2 -Math.PI/2 }"})
  donut1.setKeys(["CCY", 'PTF'], selected=1)
  donut1.setVals(["VAL", 'VAL2'])
  donut1.alertVal()

  aresObj.row([
      aresObj.col([
      aresObj.paragraph(" With the below line of Python"),
      aresObj.preformat('''
      donut1 = aresObj.donut(recordSet, header)
      donut1.addChartAttr({'startAngle': "function(d) { return d.startAngle/2 -Math.PI/2 }"})
      donut1.addChartAttr({'endAngle': "function(d) { return d.endAngle/2 -Math.PI/2 }"})
      donut1.setKeys(["CCY", 'PTF'], selected=1)
      donut1.setVals(["VAL", 'VAL2'])
      donut1.alertVal()''')])
  , donut1])


  aresObj.internalLink("Next training", 'AresExChartMultibar')