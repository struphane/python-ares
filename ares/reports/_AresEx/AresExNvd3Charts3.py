__author__ = 'HOME'


NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = []

  multiBar = aresObj.multiBar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                              headerBox='Multi Bar Chart Example', mockData=True)



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

  aresObj.row([sunburst, multiBar, stackedAreaWithFocus])
  aresObj.row([plotBox, sparklineplus])
