"""


"""

from ares.Lib.graph import AresHtmlGraphSpider
from ares.Lib import AresImports

def report(aresObj):
  aresObj.title("D3SpiderChart objects")
  aresObj.paragraph("aresObj function signature")
  aresObj.preformat('''
  spider(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False)
  ''')

  aresObj.paragraph("Reference, Javascript and CSS needs")
  impManager = AresImports.ImportManager()
  cssImports = impManager.cssResolve(AresHtmlGraphSpider.D3SpiderChart.reqCss)
  jsImports = impManager.jsResolve(AresHtmlGraphSpider.D3SpiderChart.reqJs)
  aresObj.row([aresObj.paragraph(jsImports),
               aresObj.list(AresHtmlGraphSpider.D3SpiderChart.references),
               aresObj.paragraph(cssImports)])

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
  aresObj.newline()
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
  p = aresObj.preformat('''
    chart = aresObj.spider(data, header, headerBox='Currencies')
    chart.setSeries(['CCY'])
    chart.setY(['VAL'])
    chart.setX('PRD')
  ''')
  chart = aresObj.spider(data, header, headerBox='Currencies')
  chart.setSeries(['CCY'])
  chart.setY(['VAL'])
  chart.setX('PRD')
  aresObj.row([p, chart])

  aresObj.paragraph("See the HTML source code of this page, to see the underlying javascript.")
  next = aresObj.internalLink("Next", 'AresExChartWordCloud')
  prev = aresObj.internalLink("Previous", 'AresExChartBar')
  aresObj.row([prev, next])