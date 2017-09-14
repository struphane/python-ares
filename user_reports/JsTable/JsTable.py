
AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

import string
import random
import json
import Lib.FlexFnc

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def report(aresObj):
  # Write your report here
  CCYS = ['EUR', 'GBP', 'USD']
  recordSet = []
  for i in range(5):
    recordSet.append({'ID': id_generator(), 'PTF': random.randint(1000, 1010), 'PTF2': random.randint(900, 1005),
                      'VAL2': random.uniform(0, 100),
                      'VAL3': random.uniform(0, 320),
                      'VAL': random.uniform(0, 100), 'CCY': CCYS[random.randint(0, 2)]})
  table = aresObj.table(recordSet, [[{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                     {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                                     {'key': 'VAL', 'colName': 'Value', 'colspan': 1}],
                                    [
                                      {'key': 'CCY', 'colName': 'Currency'},
                                      {'key': 'VAL2', 'colName': 'Value 2'},
                                      {'key': 'VAL3', 'colName': 'Value 3'}],
                                    ],
                        'Test Table')
  table.filters(['Currency', 'Value 2'])


  #pie = aresObj.pieChart('Folders', recordSet, {'PTF': 'Portfolio', 'PTF2': 'Portfolio 2', 'CCY': 'Currency', 'VAL': 'Value', 'VAL2': 'Value 2', 'VAL3': 'Value 3'}, selectors)
  # pie.selectCategory('Portfolio', ['Portfolio', 'Currency'], table)
  # pie.selectValues('Value 2', ['Value', 'Value 2'], table)
 # pie.linkTo(table)
 #
 #
 #  donut = aresObj.donutChart('Folders', recordSet, {'PTF': 'Portfolio', 'PTF2': 'Portfolio 2', 'CCY': 'Currency', 'VAL': 'Value', 'VAL2': 'Value 2', 'VAL3': 'Value 3'}, selectors)
 #  donut.linkTo(table)
 #  # vignet = aresObj.vignet("Super", "Voici le contenu de mq vignette", recordSet, Lib.FlexFnc.recSum, 'VAL2')
 #  # row = aresObj.row([table, pie])
 #  # row.extend(pie)
 #
 #  bar = aresObj.bar('Test', recordSet, {'PTF': 'Portfolio', 'PTF2': 'Portfolio 2', 'CCY': 'Currency', 'VAL': 'Value', 'VAL2': 'Value 2', 'VAL3': 'Value 3'}, selectors)
 #  lineChart = aresObj.lineChart('Test', recordSet,
 #                    {'PTF': 'Portfolio', 'PTF2': 'Portfolio 2', 'CCY': 'Currency', 'VAL': 'Value', 'VAL2': 'Value 2', 'VAL3': 'Value 3'}, selectors)
 #
 #  stackedAreaChart = aresObj.stackedAreaChart('Test', recordSet,
 #                    {'PTF': 'Portfolio', 'PTF2': 'Portfolio 2', 'CCY': 'Currency', 'VAL': 'Value', 'VAL2': 'Value 2', 'VAL3': 'Value 3'}, selectors)
 #
 #  stackedAreaChart.delAttr('xAxis', 'tickFormat')
 #  lineChartFocus = aresObj.lineChartFocus('Test', recordSet,
 #                                 {'ID': 'DEAL', 'PTF': 'Portfolio', 'CCY': 'Currency', 'VAL': 'Value',
 #                                  'VAL2': 'Value 2'}, selectors)
 #
 #
 #  lineChartFocus.delAttr('xAxis', 'tickFormat')
 #  lineChartFocus.delAttr('x2Axis', 'tickFormat')
 #  comboLineBar = aresObj.comboLineBar('Test', recordSet,
 #                                 {'ID': 'DEAL', 'PTF': 'Portfolio', 'CCY': 'Currency', 'VAL': 'Value',
 #                                  'VAL2': 'Value 2'}, selectors)
 #  comboLineBar.linkTo(table)
 #  comboLineBar.delAttr('xAxis', 'tickFormat')
 #  selects = {'categories': ['Portfolio', 'Currency', 'Portfolio 2'], 'selectedCats': ['Portfolio', 'Portfolio 2'], 'values': ['Value', 'Value 2', 'Value 3'], 'selectedVals': ['Value', 'Value 3']}
 #  multiBarChart = aresObj.multiBarChart('Test', recordSet,
 #                                      {'ID': 'DEAL', 'PTF': 'Portfolio', 'CCY': 'Currency', 'VAL': 'Value',
 #                                       'VAL2': 'Value 2'}, selects)
 #  multiBarChart.linkTo(table)
 #
 #  multiBarChart.delAttr('xAxis', 'tickFormat')
 #  horizBarChart = aresObj.horizBarChart('Test', recordSet,
 #                    {'PTF': 'Portfolio', 'PTF2': 'Portfolio 2', 'CCY': 'Currency', 'VAL': 'Value', 'VAL2': 'Value 2', 'VAL3': 'Value 3'}, selects)
 #
 #  horizBarChart.delAttr('xAxis', 'tickFormat')
 #  # bar.selectCategory('Portfolio', ['Portfolio', 'Currency'], table)
 #  # bar.selectValues('Value 2', ['Value', 'Value 2'], table)
 #  bar.linkTo(table)
 #  lineChart.linkTo(table)
 #  stackedAreaChart.linkTo(table)
 #  lineChartFocus.linkTo(table)
 #  horizBarChart.linkTo(table)
 #
 #  table.jsLinkTo([pie, bar])
 #  button = aresObj.button('Change Graph (Ajax)')
 #  button.post('click', '../ajax/JsTable/testAjax.py', {},
 #              '''
 #                var filterRecordSet = getDataFromRecordSet(JSON.parse(data), [%s, %s]) ;
 #                var pie = nv.models.pieChart().x(function(d) { return d[0]; }).y(function(d) { return d[1]; });
 #                d3.%s.datum(filterRecordSet).transition().duration(500).call(pie) ;
 #
 #              ''' % (pie.jqCategory, pie.jqValue, pie.jqId))
 #
 #
 #  button = aresObj.button('Change Graph (Js)')
 #  button.js('click', '''
 #                        var nRow = $('#%s thead tr')[0] ;
 #                        headers = [] ;
 #                        for (var i = 0, len = nRow.cells.length; i < len; i++) {
 #                          headers.push(nRow.cells[i].innerText) ;
 #                        };
 #
 #                        recordSet = [] ;
 #                        $("#%s").dataTable().$('tr', {"filter":"applied"}).each( function () {
 #                          var row = $(this).text().split("\\n");
 #                          rec = {};
 #                          for (var i = 0, len = headers.length; i < len; i++) {
 #                            rec[headers[i]] = row[i+1] ;
 #                          }
 #                          recordSet.push(rec) ;
 #                        } );
 #
 #                        var filterRecordSet = getDataFromRecordSet(recordSet, [%s, %s]) ;
 #                        var pie = nv.models.pieChart().x(function(d) { return d[0]; }).y(function(d) { return d[1]; });
 #                        d3.%s.datum(filterRecordSet).transition().duration(500).call(pie) ;
 #
 #                     ''' % (table.htmlId, table.htmlId, pie.jqCategory, pie.jqValue, pie.jqId))
  return aresObj
