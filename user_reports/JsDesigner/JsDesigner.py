

AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):
  # Write your report here
  aresObj.aresInput()
  aresObj.aresDragItems(['Super', 'Youpi'])
  aresObj.aresDataSource()
  return aresObj