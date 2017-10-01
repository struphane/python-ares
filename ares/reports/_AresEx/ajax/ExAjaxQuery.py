""" Ajax Data source example

As part of this example all the reports will be based on a set of mock data
Those data will only be there in order to show users how to use the different features.

It will also help them adding more interesting features by understanding well how the different
python components are working together
"""

import os
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  """ Randing String generator """
  return ''.join(random.choice(chars) for _ in range(size))


def getRecordSet(aresObj, n=20):
  """

  """
  CCYS = ['EUR', 'GBP', 'USD']
  PRODUCTS = ['Bond', 'CDS', 'TRS', 'Option', 'Index']
  recordSet = []
  for i in range(n):
    recordSet.append({'ID': id_generator(),
                      'PTF': random.randint(1, 1010),
                      'PTF2': random.randint(900, 1005),
                      'CATEGORY': PRODUCTS[random.randint(0, 4)],
                      'VAL2': random.uniform(0, 100),
                      'VAL3': random.uniform(0, 320),
                      'VAL': random.uniform(0, 100),
                      'CCY': CCYS[random.randint(0, 2)]})
  return recordSet

def call(aresObj):
  """ This will return fake data to feed the different test components in this framework """
  return getRecordSet(aresObj)