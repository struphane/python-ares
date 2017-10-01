""" [SCRIPT COMMENT]

>>>> Important variables / functions

In the python layer
    aresObj.http['FILE'] is the current file
    aresObj.http['REPORT_NAME'] is the current report environment name
    aresObj.http['DIRECTORY'] is the report location

     def readFile(self, file, subfolders=None):
     def createFile(self, file, subfolders=None, checkFileExist=True):
     def getFolders(self):
     def getFiles(self, subfolders):


In the javascript layer
    display(data) to return the result in a notification modal popup
    preloader() to show a loading page

"""


import csv
import os
import sys
import io
from WorldPopulation_data import data as csv_data


_PY3 = sys.version_info.major >= 3
_str = str if _PY3 else unicode

NAME = 'World Population' # The Report Name in the left menu
# The Shortcuts should be defined as below
# [(Cateogry Name, [List of the script in the root directory])]
# It is only possible to create new links for scripts in the root
SHORTCUTS = [] # All the possible link to other pages

def get_data():
  open_kwargs = {'newline': ''} if _PY3 else {}
  data = []

  reader = csv.reader(io.StringIO(csv_data))
  header = next(reader)

  for r in reader:
    try:
      rn = list(r[0:2])
      rn.extend([float(x) for x in r[2:]])
      
      data.append(dict(zip(header, rn)))
    except ValueError:
      pass

  del sys.modules['WorldPopulation_data']
  return data


def report(aresObj):
  data = get_data()
  meanpop = 33
  lowpop = meanpop * .25
  highpop = meanpop * 3
  areas = {}
  rc = []
  bar_rc = []
  stats = {y: dict(low=0, med=0, high=0, super=0) for y in range(1996, 2026, 10)}

  aresObj.title('World population')
  mp = aresObj.map()

  for cty in data:
    cty_name = cty['name']
    cty_code = cty['code']
    rec = {
      'code': cty_code,
      'country': cty_name
    }

    for k in cty:
      if k in ('name', 'code'):
        continue # Data contains country, code and a bunch of per-year information where `k` is the year as string

      p = cty[k] / 1000000

      if p <= lowpop:
        color = '#547044'
        cat = 'low'
      elif lowpop <= p < meanpop:
        color = '#68944f'
        cat = 'med'
      elif meanpop <= p < highpop:
        color = '#90d568'
        cat = 'super'

      stats[int(k)][cat] += 1

      p = int(_str(p).split('.')[0])
      rec.update({
        'popul-%s' % k: p,
        'cat-%s' % k: cat
      })

    area = {
      'attrs': {
        'fill': color,
        'opacity': .8
      },
      'tooltip': {
        'content': cty_name + ' ' + _str(p) + 'M'
      }
    }
    
    rc.append(rec)
    bar_rc.append({
      'y': k,
      'popul': p
    })
    areas[cty_code] = area

  dy = 2016 # Default year for initial visualisation state
  mp.update_areas(areas)
  header = [
    {'key': 'code', 'colName': 'Country Code'},
    {'key': 'country', 'colName': 'Country'}
  ]

  header.extend({ 'key': 'popul-%d' % y, 'colName': 'Population (%d)' % y} for y in range(1996, 2026, 10))

  pies = []
  pieh = [
    {'key': 'cat', 'colName': 'Category'},
    {'key': 'popul', 'colName': '# Countries', 'type': 'number'},
  ]
  cats = dict(low='Lower', med='Medium', high='High', super='Very High')
  barh = [
    {'key': 'y', 'colName': 'Year'},
    {'key': 'popul', 'colName': 'Population', 'type': 'number'}
  ]

  for y in range(1996, 2026, 10):
    piers = [{'cat': cats[cat], 'popul': n} for cat, n in stats[y].items()]
    pie = aresObj.donut(piers, pieh, headerBox=_str(y))

    pies.append(pie)

  aresObj.row([mp, aresObj.bar(piers, pieh, headerBox='Population by type')])
  aresObj.title2('Population by year')
  aresObj.row(pies)
  aresObj.title2('Population by country')
  tbl = aresObj.table(rc, header, headerBox='Population (million units)')


# The three below variables are not used anymore but they will need to be defined
# as some base classes are checking them
# A revamping will be done to remove this
REPORT_NAME = ''
AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}
