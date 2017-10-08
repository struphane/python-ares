__author__ = 'HOME'


import ExAjaxQuery

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxQuery.getRecordSet(aresObj)
  table = aresObj.table(recordSet, [
                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                        {'key': 'CCY', 'colName': 'Currency'},
                                        {'key': 'VAL2', 'colName': 'Value 2'},
                                        {'key': 'VAL3', 'colName': 'Value 3'}
                        ],
                        'Test Table')
  table.filters(['Currency', 'Value 2'])
  table.contextMenu([('Ok', 'TestScript', ['CCY']), ('Test', 'TestScript', ['VAL2'])])

  pie = aresObj.pie(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    'Chart per product')

  # To change the chart properties and only display half of the circle
  pie.addChartProp('pie', {'startAngle': 'function(d) { return d.startAngle/2 -Math.PI/2 }',
                           'endAngle': 'function(d) { return d.endAngle/2 -Math.PI/2 }'})

  #
  pie.setKeys(['CCY', 'PTF'], 'CCY')
  pie.setVals(['VAL', 'VAL3'], 'VAL')

  donut = aresObj.donut(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    'Chart per currency ')
  donut.setKeys(['CCY', 'PTF'], 'CCY')
  donut.setVals(['VAL', 'VAL3'], 'VAL')

  aresObj.row([pie, donut])
  button = aresObj.button("Refresh Data")
  button.click('ExAjaxQuery', '%s%s' % (table.jsUpdate(), pie.jsUpdate()), {})
