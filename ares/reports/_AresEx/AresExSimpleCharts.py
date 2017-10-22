__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj)

  pie = aresObj.pie(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    headerBox='Pie Chart Example', mockData=True)
  pie.setKeys(['PTF'])
  pie.setVals(['VAL'])

  donut = aresObj.donut(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                        headerBox='Donut Chart Example', mockData=True)
  donut.setKeys(['PTF'])
  donut.setVals(['VAL'])

  bar = aresObj.bar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    headerBox='Bar Chart Example', mockData=True)
  bar.setKeys(['PTF'])
  bar.setVals(['VAL'])

  horizBarChart = aresObj.horizBarChart(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                        {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                        headerBox='Horizontal Bar Chart Example', mockData=True)
  line = aresObj.line(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                        {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                      headerBox='Line Chart Example', mockData=True)
  line.setKeys(['PTF'])
  line.setVals(['VAL'])

  lineCumulative = aresObj.lineCumulative(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                          headerBox='Line Cumulative Chart Example', mockData=True)

  lineChartFocus = aresObj.lineChartFocus(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                          headerBox='Line with focus Chart Example', mockData=True)

  multiBar = aresObj.multiBar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                              headerBox='Multi Bar Chart Example', mockData=True)

  stackedArea = aresObj.stackedArea(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                    headerBox='Stacked Bar Chart Example', mockData=True)

  scatterChart = aresObj.scatter(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                 headerBox='Scatter Chart Example', mockData=True)

  sunburst = aresObj.sunburst(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                      headerBox='SunBurst Example', mockData=True)

  sparklineplus = aresObj.sparklineplus(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                    headerBox='Spark Line Plus Example', mockData=True)

  stackedAreaWithFocus = aresObj.stackedAreaWithFocus(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                    headerBox='Stacked Area with Focus Example', mockData=True)

  plotBox = aresObj.boxplot(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                    headerBox='Plot Box Example', mockData=True)

  candlestickbar = aresObj.candlestickbar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                      headerBox='Candle Stick Bar Example', mockData=True)

  forceDirected = aresObj.forceDirected(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                      headerBox='Network Example', mockData=True)

  aresObj.row([candlestickbar, forceDirected])
  aresObj.row([pie, lineCumulative, bar])
  aresObj.row([horizBarChart, line, donut])
  aresObj.row([lineChartFocus, stackedArea, scatterChart])
  aresObj.row([sunburst, multiBar, stackedAreaWithFocus])
  aresObj.row([plotBox, sparklineplus])
