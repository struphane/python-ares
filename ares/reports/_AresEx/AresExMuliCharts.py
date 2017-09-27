__author__ = 'HOME'

import ExAjaxGenerateChartRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

# Write your report here
  recordSet = ExAjaxGenerateChartRec.getRecordSet()
  barRecordSet = ExAjaxGenerateChartRec.getBarRecordset()


  aresObj.title("Basic Examples with the Charting Library")
  aresObj.paragraph('''
        The header is defined as a list of dictionary. Same as for the table
        The dictionary will use the following important keys:
            - key: the key which should be present in your recordSet of data
                   For example if you are expecting to get the below data the key can be PTF
                      recordSet = [{'serie': 'North America', 'val': 10, 'date': 1025409600000}, {'serie': 'Asia', 'val': 8, 'x': 1025409600000}]
                      (for info date values (here x) have to be in unix time epoch format
            - colName: the column header in the above example you can define the way the key names will appear in the graph = [{'key': 'serie', 'colName': 'Series'},
                                                                                                                                {'key': 'val', 'colName': 'Total'],
                                                                                                                                {'key': 'x', 'colName': 'Date'}].
            - type: Indicates how to pivot the information, if the type isn't specified:
                          - type is not specified -> the matching key will be considered part of the X Axis
                          - type = number -> the matching key will be considered part of the Y Axis
                          - type = series -> the chart will create a new serie with the matching key, in case of graph with multiple series
                          it is possible to specify the series we want to display and preselect them based on their index (if none is specifed 
                          we will select everything available by default)
                          
                          i.e : {'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['South America', 'Australia', 'Asia'],
                                 'selectedIdx': [2, 1]}]
                                 
                          Here the key serie will be used as the series and Australia and South America will be preselected when charting 
                          
                          - type = object -> this value will be ignored by the chart
                          
                          
                                                                                                                                
  
        You can see below an example of how we defined headers for the charts
        '''
                    )

  aresObj.preformat(aresObj.code('''
      headerBar = [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['North America']}]
                                
                              
      headerMultiBar = [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series'}]
                                
      lineHeader = [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['Antarctica', 'North America', 'Africa', 'South America'],
                                 'selectedIdx': [1, 3, 4]}]
      '''
    ))




  bar = aresObj.bar(barRecordSet, [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['North America']}],
                    'Graph')


  multiBar = aresObj.multiBarChart(recordSet, [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series'}],
                    'Graph')

  line = aresObj.lineChartFocus(recordSet, [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['South America', 'Australia', 'Asia'],
                                 'selectedIdx': [2, 1]}],
                    'Graph')

  horiz = aresObj.horizBarChart(recordSet, [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['Antarctica', 'North America', 'Africa', 'South America'],
                                 'selectedIdx': [1, 3, 4]}],
                    'Graph')


  scatterChart = aresObj.scatterChart(recordSet, [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['North America', 'America', 'Africa'],
                                 'selectedIdx': [1, 2, 3]}],
                    'Graph')

  stackedArea = aresObj.stackedAreaChart(recordSet, [{'key': 'Date', 'colName': 'COB Date'},
                                {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                {'key': 'serie', 'colName': 'Series', 'type': 'series', 'values': ['Europe', 'Africa'],
                                 }],
                    'Graph')

  stackedArea.style['chartAttr']['xAxis']['tickFormat'] = "function(d) { return d3.time.format('%x')(new Date(d)) }"
  line.style['chartAttr']['xAxis']['tickFormat'] = "function(d) { return d3.time.format('%x')(new Date(d)) }"

  button = aresObj.refresh("", recordSet, 'ExAjaxGenerateChartRec')
  button.click('''
                  %s ;
                  %s ;
                  %s ;
                  %s ;
                  %s ;
                  %s ;
               ''' % (bar.jsUpdate(),
                      stackedArea.jsUpdate(),
                      scatterChart.jsUpdate(),
                      horiz.jsUpdate(),
                      line.jsUpdate(),
                      multiBar.jsUpdate())
               )