
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

  button = aresObj.button('Change Graph')
  button.js('click', '''
                        
                        //alert( $('#tablerec_1').DataTable().$('tr', {"filter":"applied"}).toSource() ); ;
                        
                        $("#tablerec_1").dataTable().$('tr', {"filter":"applied"}).each( function () {
                            //var v1 = $(this).find("td:eq(0)").text();
                            var v1 = $(this).text().split("\\n");
                            alert(v1.toSource()) ;
                            } );

                        var pie = nv.models.pieChart().x(function(d) { return d[0]; }).y(function(d) { return d[1]; });
                        d3.select("#pie_3 svg").datum([['TROIS', 3], ['DEUX', 2]]).transition().duration(500).call(pie) ;

                        //nv.utils.windowResize(chart.update);
                        
                      ''')

  aresObj.pieChart('Folders', [['UN', 1], ['DEUX', 2]])
  return aresObj
