__author__ = 'HOME'

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = []

  pie = aresObj.pie(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    headerBox='Pie Chart Example', mockData=True)
  pie.setKeys(['PTF'])
  pie.setVals(['VAL'])

  bar = aresObj.bar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    headerBox='Bar Chart Example', mockData=True)
  bar.setKeys(['PTF'])
  bar.setVals(['VAL'])

  lineCumulative = aresObj.lineCumulative(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                          headerBox='Line Cumulative Chart Example', mockData=True)

  candlestickbar = aresObj.candlestickbar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                      headerBox='Candle Stick Bar Example', mockData=True)

  forceDirected = aresObj.forceDirected(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                      headerBox='Network Example', mockData=True)

  aresObj.row([candlestickbar, forceDirected])
  aresObj.row([pie, lineCumulative, bar])

