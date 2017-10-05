__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj)

  aresObj.paragraph('''
          The header is defined as a list of dictionary. Same as for the table
          The dictionary will use the following important keys:
              - key: the key which should be present in your recordSet of data
              - colName: the column header in the above example you can define the way the key names will appear in the graph = [{'key': 'val', 'colName': 'Total'], {'key': 'x', 'colName': 'Date'}].
              - type: Indicates how to pivot the information, if the type isn't specified:
                            - type is not specified -> the matching key will be considered part of the X Axis
                            - type = number -> the matching key will be considered part of the Y Axis
                            - type = object -> this value will be ignored by the chart

          You can see below an example of how we defined headers for the pie charts 
          You can have two types of Pie Charts -> Donut (donut) or Plain (pie)
          '''
                    )

  aresObj.preformat(aresObj.code('''
        headerBar = [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}]


        recordSet = %s
        ''' % recordSet
                                 ))

  #pie = aresObj.pie(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
  #                              {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
  #                   'Graph')

  donut = aresObj.stackedAreaChart(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    'Graph')

  #button = aresObj.refresh("", recordSet, 'ExAjaxRec')
  #button.click('''
  #                %s ;
  #                %s ;
  #             ''' % (donut.jsUpdate(), pie.jsUpdate())
  #             )