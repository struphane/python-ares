__author__ = 'HOME'

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = []
  donut = aresObj.donut(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                        headerBox='Donut Chart Example', mockData=True)

  horizBarChart = aresObj.horizBar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                        {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                        headerBox='Horizontal Bar Chart Example', mockData=True)
  line = aresObj.line(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                        {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                      headerBox='Line Chart Example', mockData=True)

  lineChartFocus = aresObj.lineChartFocus(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                          headerBox='Line with focus Chart Example', mockData=True)

  stackedArea = aresObj.stackedArea(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                    headerBox='Stacked Bar Chart Example', mockData=True)

  scatterChart = aresObj.scatter(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                 headerBox='Scatter Chart Example', mockData=True)

  aresObj.row([horizBarChart, line, donut])
  aresObj.row([lineChartFocus, stackedArea, scatterChart])

