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

def report(aresObj):
  """ Main function to build the reports

  In this section it is important to change the object aresObj in order to produce the right HTML page
  This content will be directly added to the page in order to display the results in a properly formed HTML pages
  All the header section and footer will be automatically generated on the server side.

  By running the script locally partial files will be generated
  """

  dropComp = aresObj.dropdown([['Super', ('A', 'a'), ('B', 'b')]])
  dropComp.js('click', 'alert($(this).text()) ; ')

  textComp = aresObj.textArea('')
  textComp.js('click', 'alert(%s) ; ' % textComp.jsVal())
  zoneComp = aresObj.dropzone('Drop Files')

  spId = aresObj.select([('Node', ['GBC', 'BNPPAR'])])
  #aresObj.item(spId).jsAjax('change', textComp.text('data'), 'MyRepotTestAjax.py', '', {})

  divComp =  aresObj.div("Olivier")
  #aresObj.anchor('Great link to a new page', aresObj.http['FILE'], 'test', CHILD_PAGES, localPath)
  #aresObj.anchor('Great link to a new page, Again and Again', aresObj.http['FILE'], 'test3', CHILD_PAGES, localPath)
  # Section put in a container
  listComp = aresObj.listbadge([('test', 1), ('Aurelie', 12)])
  tableComp = aresObj.table([['Olivier', 'Aurelie', 'Youpi'], [1, 2, 'super'], [3, 4, 'encore']])
  aresObj.grid([listComp, tableComp])
  aresObj.title('Test Report Header')
  aresObj.title2('sub Title')
  aresObj.button('Youpi Test', 'btn-success')
  inComp = aresObj.input('test', 'Encore')
  #inComp.js('blur', 'alert("I can update the DB") ;')
  fontComp = aresObj.text('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYOUPI', 'font-weight-bold')
  aresObj.paragraph('Voici mon result {0}', [fontComp])
  divComp.js('click', ' %s.html(%s);' % (fontComp.jsRef(), spId.jsVal()))
  aresObj.title3('sub Title 2')
  aresObj.title4('Title 2')
  aresObj.title2('Sub Title Test')
  #cloudId = aresObj.cloudChart([('Super', 10), ('Olivier', 20), ('Aurelie', 20)])
  #pieDi = aresObj.pieChart([("One", 29.765957771107), ("Two", 32.807804682612)  ])
  #aresObj.grid(aresObj.item(cloudId), aresObj.item(pieDi))

  #aresObj.addNavigationBar(width=15)
  #data = [{'key': 'NVD3', 'url': 'http://novus.github.com/nvd3', 'values': [{'key': "Charts", '_values': [{
  #          'key': "Simple Line", 'type': "Historical", 'url': "http://novus.github.com/nvd3/ghpages/line.html"
  #          }] }]
  #         }],
  #cols = [{'key': 'type', 'label': 'Type', 'width': '25%', 'type': 'text'}]
  #aresObj.tree(cols, data)
  #aresObj.stackedAreaChart(None, useMockData=False)
  #aresObj.multiBarChart(None, useMockData=False)
  #aresObj.lineChart(None, useMockData=False)
  #aresObj.comboLineBar(None, useMockData=False)

  #aresObj.horizBarChart(None, useMockData=True)

  return aresObj