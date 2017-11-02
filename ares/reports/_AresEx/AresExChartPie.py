"""


"""

from ares.Lib.graph import AresHtmlGraphPie

def report(aresObj):
  aresObj.title("NvD3Pie and NvD3Donut objects")
  aresObj.paragraph("aresObj function signature")
  aresObj.preformat('''
  def donut(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False)
  def pie(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False)
  ''')

  aresObj.paragraph("References")
  aresObj.list(AresHtmlGraphPie.NvD3Pie.references)
  aresObj.newline()

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

  aresObj.paragraph("Example of value and header")
  aresObj.preformat('''
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
  ''')

  aresObj.paragraph("Display the chart")
  aresObj.preformat('''
    chart = aresObj.pie(data, header, headerBox='Currencies')
    chart.setKeys(['CCY', 'COB'])
    chart.setVals(['VAL'])
  ''')

  chart = aresObj.pie(data, header, headerBox='Currencies')
  chart.setKeys(['CCY', 'COB'])
  chart.setVals(['VAL'])
  chart.changeColor(["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"])

  chart2 = aresObj.donut(data, header, headerBox='Currencies')
  chart2.setKeys(['CCY', 'COB'])
  chart2.setVals(['VAL'])

  aresObj.row([aresObj.col([aresObj.paragraph('Pie Chart'), chart]),
               aresObj.col([aresObj.paragraph('Donut Chart'), chart2])])

  aresObj.paragraph("Display a 2D pie chart with multiple keys and values")
  chart3 = aresObj.pie(data, header, headerBox='Currencies')
  chart3.setKeys(["CCY", 'PTF'], selected=1)
  chart3.setVals(["VAL", 'VAL2'])

  aresObj.row([
    aresObj.preformat('''
    chart3 = aresObj.pie(data, header, headerBox='Currencies')
    chart3.setKeys(["CCY", 'PTF'], selected=1)
    chart3.setVals(["VAL", 'VAL2'])
                      '''), chart3])

  donut1 = aresObj.donut(data, header)
  donut1.addChartAttr({'startAngle': "function(d) { return d.startAngle/2 -Math.PI/2 }"})
  donut1.addChartAttr({'endAngle': "function(d) { return d.endAngle/2 -Math.PI/2 }"})
  donut1.setKeys(["CCY", 'PTF'], selected=1)
  donut1.setVals(["VAL", 'VAL2'])
  donut1.alertVal()
  aresObj.paragraph("Change the style of the chart")
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

  aresObj.paragraph("See the HTML source code of this page, to see the underlying javascript.")
  aresObj.internalLink("Next", 'AresExChartBar')