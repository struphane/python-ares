""" Report Module

"""

CHILD_PAGES = {} # No Child for this page

def report(aresObj, localPath=None):
  """ Empty report with only a title """
  aresObj.title(1, '%s I am a child %s' % (aresObj.http['GET']['myvar'], aresObj.http['GET']['var2']))
  return aresObj
	