__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj)

  pie = aresObj.pie(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    headerBox='Pie Chart Example')

  donut = aresObj.donut(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                        headerBox='Donut Chart Example')

  bar = aresObj.bar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    headerBox='Bar Chart Example')

  horizBarChart = aresObj.horizBarChart(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                        {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                        headerBox='Horizontal Bar Chart Example')

  line = aresObj.line(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                        {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                      headerBox='Line Chart Example')

  lineCumulative = aresObj.lineCumulative(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                          headerBox='Line Cumulative Chart Example')


  lineChartFocus = aresObj.lineChartFocus(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                          headerBox='Line with focus Chart Example')

  multiBar = aresObj.multiBar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                              headerBox='Multi Bar Chart Example')

  stackedArea = aresObj.stackedArea(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                    headerBox='Stacked Bar Chart Example')


  scatterChart = aresObj.scatter(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                 headerBox='Scatter Chart Example')


  sunburst = aresObj.sunburst(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                      headerBox='SunBurst Example')

  sparklineplus = aresObj.sparklineplus(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                    headerBox='Spark Line Plus Example')

  stackedAreaWithFocus = aresObj.stackedAreaWithFocus(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                    headerBox='Stacked Area with Focus Example')

  plotBox = aresObj.boxplot(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                    headerBox='Plot Box Example')

  candlestickbar = aresObj.candlestickbar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                      headerBox='Candle Stick Bar Example')


  forceDirected = aresObj.forceDirected(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                                      headerBox='Network Example')
  aresObj.row([candlestickbar, forceDirected])
  aresObj.row([pie, lineCumulative, bar])
  aresObj.row([horizBarChart, line, donut])
  aresObj.row([lineChartFocus, stackedArea, scatterChart])
  aresObj.row([sunburst, multiBar, stackedAreaWithFocus])
  aresObj.row([plotBox, sparklineplus])
