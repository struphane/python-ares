
AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def report(aresObj):
  # Write your report here
  CCYS = ['EUR', 'GBP', 'USD']
  recordSet = []
  for i in range(5):
    recordSet.append({'ID': id_generator(), 'PTF': random.randint(1000, 1010), 'VAL': random.uniform(0, 100), 'CCY': CCYS[random.randint(0, 2)]})
  table = aresObj.tableRec('My Table', recordSet, {'PTF': 'Portfolio', 'CCY': 'Currency', 'VAL': 'Value'})
  table.filters({'Currency': 'CCY'})

  pie = aresObj.pieChart('Folders', [])

  button = aresObj.button('Change Graph (Ajax)')
  button.post('click', '../ajax/JsTable/testAjax.py', {},
              '''
                var pie = nv.models.pieChart().x(function(d) { return d[0]; }).y(function(d) { return d[1]; });
                d3.%s.datum(JSON.parse(data)).transition().duration(500).call(pie) ;

              ''' % pie.jqId)


  button = aresObj.button('Change Graph (Js)')
  button.js('click', '''
                        var nRow = $('#%s thead tr')[0] ;
                        headers = [] ;
                        for (var i = 0, len = nRow.cells.length; i < len; i++) {
                          headers.push(nRow.cells[i].innerText) ;
                        };
                        
                        recordSet = [] ;
                        $("#%s").dataTable().$('tr', {"filter":"applied"}).each( function () {
                          var row = $(this).text().split("\\n");
                          rec = {};
                          for (var i = 0, len = headers.length; i < len; i++) {
                            rec[headers[i]] = row[i+1] ; 
                          }
                          recordSet.push(rec) ;
                        } );
                        
                        var filterRecordSet = getDataFromRecordSet(recordSet, ['Portfolio', 'Value']) ;
                        var pie = nv.models.pieChart().x(function(d) { return d[0]; }).y(function(d) { return d[1]; });
                        d3.%s.datum(filterRecordSet).transition().duration(500).call(pie) ;

                     ''' % (table.htmlId, table.htmlId, pie.jqId))
  return aresObj
