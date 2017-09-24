""" Example module for the HTML Table objects

"""

import ExAjaxRec

NAME = 'Complex Tables'

def report(aresObj):
  """
  Example of a report to explain and show how to use HTML tables in a report.
  It will describe the part to write but also what will be done behind the scene to ensure the web browser can get
  the data
  """
  # Produce the recordSet
  recordSet = ExAjaxRec.getRecordSet()
  table = aresObj.table(recordSet, [
                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                    {'key': 'CCY', 'colName': 'Currency'},
                                    {'key': 'VAL2', 'colName': 'Value 2'},
                                    {'key': 'VAL3', 'colName': 'Value 3'}
                        ],
                        'Test Table')

  # Special properties of the HTML object
  table.filters(['Currency', 'Value 2'])
  table.contextMenu([('Link to Currency', 'AresExTableLinkCcy', ['CCY']), ('Link to Ptf and Currency', 'AresExTableLinkCcyPtf', ['PTF', 'CCY'])])
  table.click(
    '''
    alert( 'You clicked on ' + rowData[0].PTF + ' row' );
    '''
  )
