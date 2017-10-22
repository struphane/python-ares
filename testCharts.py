
from Lib import AresChartsService


data = [{"CCY": 'GBP', 'VAL': 100},
        {"CCY": 'GBP', 'VAL': 40},
        {"CCY": 'EUR', 'VAL': 23},
        {"CCY": 'USD', 'VAL': 66}]


print(AresChartsService.toBar(data, 'Currency View', 'CCY', 'VAL'))


print(AresChartsService.toPie(data, 'CCY', 'VAL'))