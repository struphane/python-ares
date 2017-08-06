"""
This is the main page for the report.

Users will start with this page then they will navigate to get the other pages.
The minimum to create a report is

AJAX_CALLS = {} # No Ajax call
CHILD_PAGES = {} # No Child page

def report(aresObj, localPath=None):
  ...
  return aresObj.html(localPath, title='Report Title')

"""

# This list should contain the tuple (alias, scriptName
# Thanks to this the script should behave the same locally and on the server.
# The only different is that the wrapper will locally create the different child pages (in html) instead
# of generating them on the fly from Flask
AJAX_CALLS = [
  'MyRepotTestAjax.py'
  ]

# Currently this is only supported by the anchor balises
# If there is button and actions we will assume that this will be sent via Ajax calls
CHILD_PAGES = {
	'test': 'MyRepotTestChild.py',
  'test3': 'MyRepotTestChild3.py',
  }

def report(aresObj, localPath=None):
  """ Main function to build the reports

  In this section it is important to change the object aresObj in order to produce the right HTML page
  This content will be directly added to the page in order to display the results in a properly formed HTML pages
  All the header section and footer will be automatically generated on the server side.

  By running the script locally partial files will be generated
  """

  bpId = aresObj.dropDown('Super', [('A', 'a'), ('B', 'b')])
  aresObj.item(bpId).js('click', 'alert($(this).text()) ; ')

  areaId = aresObj.textArea()
  aresObj.item(areaId).click('alert(%s) ; ' % aresObj.item(areaId).jsVal())
  dropId = aresObj.dropZone()

  spId = aresObj.select([('Node', ['GBC', 'BNPPAR'])])
  aresObj.item(spId).jsAjax('change', aresObj.item(areaId).text('data'),
                            'MyRepotTestAjax.py', localPath, {})

  bId =  aresObj.div("Olivier")
  # aresObj.anchor('Great link to a new page', 'test', CHILD_PAGES, localPath)
  # aresObj.anchor('Great link to a new page, Again and Again', 'test3', CHILD_PAGES, localPath)
  # Section put in a container
  lId = aresObj.list([('test', 1), ('Aurelie', 12)])
  tId = aresObj.table(['Olivier', 'Aurelie', 'Youpi'], [[1, 2, 'super'], [3, 4, 'encore']])
  aresObj.grid(aresObj.item(lId), aresObj.item(tId))
  aresObj.title(1, 'Test Report Header')
  aresObj.title(2, 'sub Title')
  bId = aresObj.button('Youpi Test', 'btn-success')
  iId2 = aresObj.input('test', 'Encore')
  aresObj.item(iId2).js('blur', 'alert("I can update the DB") ;')

  tId = aresObj.text('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYOUPI', 'font-weight-bold')
  aresObj.paragraph('Voici mon result {0}', [aresObj.item(tId)])
  aresObj.item(bId).js('click', ' %s.html(%s);' % (aresObj.item(tId).jsRef(), aresObj.item(iId2).jsVal()))
  aresObj.title(3, 'sub Title 2')
  aresObj.title(1, 'Title 2')
  aresObj.title(2, 'Sub Title Test')
  cloudId = aresObj.cloudChart([('Super', 10), ('Olivier', 20), ('Aurelie', 20)])
  pieDi = aresObj.pieChart([("One", 29.765957771107), ("Two", 32.807804682612)  ])
  aresObj.grid(aresObj.item(cloudId), aresObj.item(pieDi))

  aresObj.addNavigationBar(width=15)
  data = [{'key': 'NVD3', 'url': 'http://novus.github.com/nvd3', 'values': [{'key': "Charts", '_values': [{
            'key': "Simple Line", 'type': "Historical", 'url': "http://novus.github.com/nvd3/ghpages/line.html"
            }] }]
           }],
  cols = [{'key': 'type', 'label': 'Type', 'width': '25%', 'type': 'text'}]
  aresObj.tree(cols, data)
  #aresObj.stackedAreaChart(None, useMockData=False)
  #aresObj.multiBarChart(None, useMockData=False)
  #aresObj.lineChart(None, useMockData=False)
  #aresObj.comboLineBar(None, useMockData=False)

  #aresObj.horizBarChart(None, useMockData=True)

  return aresObj