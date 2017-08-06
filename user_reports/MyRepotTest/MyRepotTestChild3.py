""" Report Module

"""

import string
import random

CHILD_PAGES = {} # No Child for this page

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  """ Generate random strings """
  return ''.join(random.choice(chars) for _ in range(size))

def report(aresObj, localPath=None):
  """ Empty Report with only a title """
  aresObj.title(1, 'I am a child 3')
  data = [(id_generator(), random.randint(5, 35)) for i in range(10)]
  aresObj.cloudChart(data) # Add a Cloud Chart
  return aresObj.html(localPath, title='Fourth Page')
