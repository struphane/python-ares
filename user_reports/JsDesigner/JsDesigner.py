

AJAX_CALL = {} # ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):
  # Write your report here
  input  = aresObj.aresInput()
  drags = aresObj.aresDragItems(aresObj.components())
  left = aresObj.col([input, drags])


  tabs = aresObj.tabs(['HTML', 'Python'])
  drop = aresObj.aresDataSource(cssCls='page')
  right = aresObj.col([tabs, drop])

  row = aresObj.row([left, right])
  row.extend(tabs)
  return aresObj