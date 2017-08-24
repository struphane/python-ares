

AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):
  # Write your report here
  title = aresObj.title("This is my first report !!!")
  table = aresObj.table('My Table', [['Youpi'], ['test']])
  title2 = aresObj.title2("")
  input = aresObj.input()
  input.js('change', '')

  input.jsLinkTo([title, title2, table])
  return aresObj
