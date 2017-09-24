


import ExAjaxDataExtract

NAME = 'Reports Data Extract'

def report(aresObj):
  """
  """
  aresObj.title('Report Data Extraction')

  dateObj = aresObj.date('COB Date')
  nodeObj = aresObj.input('Node')
  nameObj = aresObj.input('Name')
  button = aresObj.button("Extract Data")

