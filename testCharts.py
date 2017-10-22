"""

"""

from Lib import AresChartsService
from ares.Lib.graph import AresHtmlGraphPie
from ares.Lib import Ares

data = [{"CCY": 'GBP', 'VAL': 100, 'COB': '2017-10-20'},
        {"CCY": 'GBP', 'VAL': 40, 'COB': '2017-10-21'},
        {"CCY": 'EUR', 'VAL': 23, 'COB': '2017-10-19'},
        {"CCY": 'USD', 'VAL': 66, 'COB': '2017-10-21'}]

header = [
  {'key': "CCY", 'colName': 'Currency'},
  {'key': "VAL", 'colName': 'Value'},
  {'key': "COB", 'colName': 'Close of Business'}
]
#print(AresChartsService.toBar(data, 'Currency View', 'CCY', 'VAL'))


#print(AresChartsService.toPie(data, 'CCY', 'VAL'))


#print(AresChartsService.toStackedArea(data, 'CCY', 'COB', 'VAL', isXDt='%Y-%m-%d', seriesNames={'EUR': 'Time series for Euro'}))

aresObj = Ares.Report()
pie = AresHtmlGraphPie.NvD3Pie(aresObj, "test", data, header)
pie.setKeys(['CCY'])
pie.setVals(['VAL'])
pie.graph()
str(pie)
print(aresObj.jsGraphs)
