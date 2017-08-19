''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):

  aresObj.title("IRC Results for %s" % aresObj.http['GET']['NODE'])
  uploadComp = aresObj.upload()
  uploadComp.js('change', '')
  aresObj.pieChart('', [["One", 29],["4fdffgfd", 196]])
  aresObj.pieChart('', [["One", 1119],["Four", 5],["youpi", 5]])
  return aresObj