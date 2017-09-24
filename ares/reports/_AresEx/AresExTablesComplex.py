""" Example module for the HTML Table objects

"""

import ExAjaxRec

NAME = 'Tables'

def report(aresObj):
  """
  Example of a report to explain and show how to use HTML tables in a report.
  It will describe the part to write but also what will be done behind the scene to ensure the web browser can get
  the data
  """
  # Produce the recordSet
  recordSet = ExAjaxRec.getRecordSet()
  table = aresObj.table(recordSet, [
                                    [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                     {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                                     {'key': 'VAL', 'colName': 'Value', 'colspan': 2}],

                                     [{'key': 'PTF3', 'colName': 'Portfolio 3'},
                                      {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                                      {'key': 'VAL1', 'colName': 'Value 1', 'colspan': 1}],

                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                        {'key': 'CCY', 'colName': 'Currency'},
                                        {'key': 'VAL2', 'colName': 'Value 2'},
                                        {'key': 'VAL3', 'colName': 'Value 3'}
                        ],
                        'Test Table')
  # Special properties of the HTML object
  table.filters(['Currency', 'Value 2'])
  table.contextMenu([('Ok', 'TestScript', ['CCY']), ('Test', 'TestScript', ['VAL2'])])
  table.click(
    '''
    var rowData = %s.rows($(this)[0]._DT_RowIndex).data();
        alert( 'You clicked on ' + rowData[0].script + ' row' );
        }
    '''
  )
