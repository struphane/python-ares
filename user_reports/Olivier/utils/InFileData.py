"""

"""

from Libs import AresFileParser

class InFileMyData(AresFileParser.FileParser):
  """
  """
  delimiter = ','
  hdrLines = 1

  cols = [
      {'colName': 'CCY'},
      {'colName': 'PRD'},
      {'colName': 'VAL'},
      {'colName': 'COB'},
      {'colName': 'VAL2'},
      {'colName': 'PTF'}]