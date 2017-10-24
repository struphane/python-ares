""" Example module for the HTML Table objects

"""

import ExAjaxRec

NAME = 'Tables'
DOWNLOAD = 'SCRIPT'

def report(aresObj):
  """
  Example of a report to explain and show how to use HTML tables in a report.
  It will describe the part to write but also what will be done behind the scene to ensure the web browser can get
  the data
  """
  # Produce the recordSet
  recordSet = ExAjaxRec.getRecordSet(aresObj)
  aresObj.title("Basic Table with Multiple headers")
  aresObj.paragraph('''
    The header is defined as a list of dictionary.
    The dictionary will use two important keys:
        - key: the key which should be present in your recordSet of data
               For example if you are expecting to get the below data the key can be PTF
                  recordSet = [{'PTF': 1, 'VAL': 10}, {'PTF': 2, 'VAL': 2}]
        - colName: the column header in the above example you can define header = [{'key': 'PTF', 'colName': 'Portfolio'}]

    In the table display below the header is defined as below:
    '''
  )
  aresObj.preformat(aresObj.code('''
    header = [ {'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
               {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
               {'key': 'VAL', 'colName': 'Value', 'colspan': 2}],

               [{'key': 'PTF3', 'colName': 'Portfolio 3'},
                {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                {'key': 'VAL1', 'colName': 'Value 1', 'colspan': 1}],

              [{'key': 'PTF', 'colName': 'Portfolio'},
                  {'key': 'CCY', 'colName': 'Currency'},
                  {'key': 'VAL2', 'colName': 'Value 2'},
                  {'key': 'VAL3', 'colName': 'Value 3'}]
    '''
  ))

  aresObj.title3("Result")
  table = aresObj.table(recordSet, [
                                    [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                     {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                                     {'key': 'VAL', 'colName': 'Value', 'colspan': 2}],

                                     [{'key': 'PTF3', 'colName': 'Portfolio 3'},
                                      {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                                      {'key': 'VAL1', 'colName': 'Value 1', 'colspan': 1}],

                                    [{'key': 'PTF', 'colName': 'Portfolio'},
                                        {'key': 'CCY', 'colName': 'Currency'},
                                        {'key': 'VAL2', 'colName': 'Value 2'},
                                        {'key': 'VAL3', 'colName': 'Value 3'}]
                        ],
                        'Test Table')
  table.callBackHideHeader()
  table.callBackCreateRowThreshold('VAL3', 50, 'btn-success')
  table.click('alert(rowData)') #, 2, 'CCY')
  table.option('pageLength' , 10)
  table.callBackRow('CCY', 'GBP', 'yellow')
  table.columnDefs([{"targets": [2], "visible": False, "searchable": False}])
  #table.click('alert(rowData)')
  table.callBackFooterColumns([])
  #table.callBackCreateRowHideFlag('CCY', 'GBP')

