''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',} 

def report(aresObj):
  aresObj.button('Youpi')
  aresObj.date('2015-04-02')

  return aresObj