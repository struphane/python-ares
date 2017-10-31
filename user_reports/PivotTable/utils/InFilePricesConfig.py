"""

"""

from Libs import AresFileParser

def TryFloat(val):
  try:
    return float(val)
  except:
    return 0

class InFilePices(AresFileParser.FileParser):
  """
  """
  delimiter = ','
  hdrLines = 1

  cols = [
      {'colName': 'CODE'},
      {'colName': 'TYPE'},
      {'colName': 'EXERCISE', 'convertFnc': TryFloat},
      {'colName': 'EXPIRY'},
      {'colName': 'RATIO'},
      {'colName': 'EX STYLE'},
      {'colName': 'ISSUER'},
      {'colName': 'REGISTRY'},
      {'colName': 'LISTED'},
      {'colName': 'ISSUED (M)'},
      {'colName': 'NOTES'}]

