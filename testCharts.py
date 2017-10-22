"""

"""

from Lib import AresChartsService


data = [{"CCY": 'GBP', 'VAL': 100, 'COB': '2017-10-20'},
        {"CCY": 'GBP', 'VAL': 40, 'COB': '2017-10-21'},
        {"CCY": 'EUR', 'VAL': 23, 'COB': '2017-10-19'},
        {"CCY": 'USD', 'VAL': 66, 'COB': '2017-10-21'}]


#print(AresChartsService.toBar(data, 'Currency View', 'CCY', 'VAL'))


#print(AresChartsService.toPie(data, 'CCY', 'VAL'))


print(AresChartsService.toStackedArea(data, 'CCY', 'COB', 'VAL', isXDt='%Y-%m-%d', seriesNames={'EUR': 'Time series for Euro'}))