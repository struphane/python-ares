"""

"""


# No Child for this page
CHILD_PAGES = {
  'test2': 'MyRepotTestChild2.py'
}

def report(aresObj, localPath=None):
  """
  """
  aresObj.title(1, 'I am a child')
  aresObj.anchor('Great link to a new page, again !', aresObj.http['FILE'], 'test2?myvar=great!!!!&var2=10', CHILD_PAGES, localPath)
  return aresObj
	