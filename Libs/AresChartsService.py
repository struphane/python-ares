""" Service dedicated to convert your recordSet to an object that your graph will recognise
@author: Olivier Nogues

This module is the interface to translate your raw data.
The right way to use this interface is to locally directly import it (as no ajax call will be possible locally.
All the interaction with a server will require the scripts (Ajax/Services) deployed to the server (and obviously an internet
connection).

Nevertheless by importing this module locally you can extract your raw data and benefit from all the interactive
features available in the charts directly from NVD3. Basically you can focus on some parts of the charts or filter some
data. only the functions which will change your raw data might not work.

In any services dedicated to provide data to a chart, please ensure this module is used. Indeed if there is any change
in the chart interface in the future your report will not be impacted as this interface will handle the change !

"""

import re
import time
import datetime
import collections

regex = re.compile('[^a-zA-Z0-9_]')

def to2DCharts(recordSet, seriesName, keysWithFormat, valsWithFormat, extKeys=None):
  """ Function dedicated to return from a recordSet for the 2D charts with single series

  The key and val should be some keys defined in the recordSet.
  The values should be float data and the seriesName should be the name that you would like to display in your chart
  """
  data = collections.defaultdict(lambda: collections.defaultdict(float))
  trsnsfValFormat = []
  for val, valFormat, multiplier in valsWithFormat:
    if valFormat is None:
      trsnsfValFormat.append((val, float, multiplier))
    else:
      trsnsfValFormat.append((val, {'int': int, 'float': float, 'number': float}[valFormat], multiplier))

  if extKeys is None:
    data = collections.defaultdict(lambda: collections.defaultdict(float))
    for key, format, _ in keysWithFormat:
      if format is not None: # If there is a timestamp format defined
        # Python uses seconds in the timestamp whereas javascript uses the mili seconds
        mapFnc = lambda dt, dtFmt: int(datetime.datetime.strptime(dt, dtFmt).timestamp()) * 1000
      else:
        mapFnc = lambda dt, dtFmt: str(dt)
      for rec in recordSet:
        for val, valFormat, multiplier in trsnsfValFormat:
          data[(key, val)][mapFnc(rec[key], format)] += valFormat(rec[val]) * multiplier

    resultSets = {}
    for key, aggVals in data.items():
      result = [{'key': seriesName, 'values': []}]
      sortedDt = sorted(aggVals.keys())
      for dataKey in sortedDt:
        result[0]['values'].append({ 'key': dataKey,  'value': aggVals[dataKey] })
      resultSets["_".join(key)] = result
  else:
    data = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(float)))
    for key, format, _ in keysWithFormat:
      if format is not None: # If there is a timestamp format defined
        # Python uses seconds in the timestamp whereas javascript uses the mili seconds
        mapFnc = lambda dt, dtFmt: int(datetime.datetime.strptime(dt, dtFmt).timestamp()) * 1000
      else:
        mapFnc = lambda dt, dtFmt: str(dt)
      for rec in recordSet:
        for val, valFormat, multiplier in trsnsfValFormat:
          extkeyResolve = regex.sub('', "_".join([rec[extKey] for extKey in extKeys]))
          data[extkeyResolve][(key, val)][mapFnc(rec[key], format)] += valFormat(rec[val]) * multiplier
    resultSets = {}
    for extKeys, recordSet in data.items():
      for key, aggVals in recordSet.items():
        result = [{'key': seriesName, 'values': []}]
        sortedDt = sorted(aggVals.keys())
        for dataKey in sortedDt:
          result[0]['values'].append( { 'key': dataKey, 'value': aggVals[dataKey] } )
        resultSets["%s_%s" %(extKeys, "_".join(key))] = result
  return resultSets

def toMultiSeriesChart(recordSet, keysWithFormat, xWithFormat, valsWithFormat, seriesNames=None, extKeys=None):
  """ Function dedicated to handle charts with multiple series

  In those chart each series will have a certain numboer of points and the series name might be defined.
  Basically the x will be the series x abscisse, it will correspond to a key in the recordset and it can be
  converted to a timestamp if a isXDt format is defined. By default we will keep the value defined in the recordset
  Please have a look at the different keys possible:

  For example 2017-10-20 will be defined with a format %Y-%m-%d
  https://www.tutorialspoint.com/python/time_strptime.htm

  The special mapping table seriesNames, will allow to define propername for the series keys possible in the recordset
  """
  if xWithFormat[1] is not None: # If there is a timestamp format defined
    # Python uses seconds in the timestamp whereas javascript uses the mili seconds
    mapFnc = lambda dt, dtFmt: int(time.mktime(datetime.datetime.strptime(dt, dtFmt).timetuple())) * 1000
  else:
    mapFnc = lambda dt, dtFmt: str(dt)

  trsnsfValFormat = []
  for val, valFormat, multiplier in valsWithFormat:
    if valFormat is None:
      trsnsfValFormat.append((val, float, multiplier))
    else:
      trsnsfValFormat.append((val, {'int': int, 'float': float, 'number': float}[valFormat], multiplier))

  if extKeys is None:
    # Define the temporary dataSet used to aggregate the data in the recordSet
    data = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
    # Aggregate the data in the recordSet
    for key, keyFormat, _ in keysWithFormat:
      for rec in recordSet:
        dt = mapFnc(rec[xWithFormat[0]], xWithFormat[1]) # Use the map function
        for val, valFormat, multiplier in trsnsfValFormat:
          data[(key, val)][rec[key]][dt] += valFormat(rec[val]) * multiplier
    # Produce the final data structure required by the multi series charts
    resultSets = {}
    for rawKey, aggVals in data.items():
      result = []
      for key, series in aggVals.items():
        seriesData = {'key': seriesNames.get(key, key) if seriesNames is not None else key, 'values': []}
        sortedDt = sorted(series.keys())
        for dt in sortedDt:
          seriesData['values'].append([dt, series[dt]])
        result.append(seriesData)
      resultSets["_".join(rawKey)] = result
  else:
    # Define the temporary dataSet used to aggregate the data in the recordSet
    data = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int))))
    # Aggregate the data in the recordSet
    for key, keyFormat, _ in keysWithFormat:
      for rec in recordSet:
        dt = mapFnc(rec[xWithFormat[0]], xWithFormat[1]) # Use the map function
        for val, valFormat, multiplier in trsnsfValFormat:
          extkeyResolve = regex.sub('', "_".join([rec[extKey] for extKey in extKeys]))
          data[extkeyResolve][(key, val)][rec[key]][dt] += valFormat(rec[val]) * multiplier
    # Produce the final data structure required by the multi series charts
    resultSets = {}
    for extKeys, recordSet in data.items():
      for rawKey, aggVals in recordSet.items():
        result = []
        for key, series in aggVals.items():
          seriesData = {'key': seriesNames.get(key, key) if seriesNames is not None else key, 'values': []}
          sortedDt = sorted(series.keys())
          for dt in sortedDt:
            seriesData['values'].append([dt, series[dt]])
          result.append(seriesData)
        resultSets["%s_%s" % (extKeys, "_".join(rawKey))] = result
  return resultSets


# ------------------------------------------------------------------------------
# Interface for the different Simple SVG charts
# ------------------------------------------------------------------------------
def toPie(recordSet, key, val, extKeys=None):
  """ Function dedicated to the Pie Chart and the Donut chart

  """
  data = dict([(key, result[0]['values']) for key, result in to2DCharts(recordSet, None, key, val, extKeys=extKeys).items()])
  return data

def toBar(recordSet, seriesName, key, val, extKeys=None):
  """ Function dedicated to the Bar Chart """
  return to2DCharts(recordSet, seriesName, key, val, extKeys=extKeys)

def toWordCloud(recordSet, key, val, extKeys=None):
  """ Function dedicated to the World Cloud Chart """
  data = {}
  for key, result in to2DCharts(recordSet, None, key, val, extKeys=extKeys).items():
    data[key] = [{'text': text, 'size': int(size)} for text, size  in result[0]['values']]
  return data


# ------------------------------------------------------------------------------
# Interface for the different Multi charts
# ------------------------------------------------------------------------------
def toMultiSeries(recordSet, key, x, val, seriesNames=None, extKeys=None):
  """ Function dedicated to the StackedArea Chart

  https://www.tutorialspoint.com/python/time_strptime.htm
  """
  return toMultiSeriesChart(recordSet, key, x, val, seriesNames, extKeys)

def toComboChart(recordSet, key, x, val, seriesNames=None, barStyle=None, colors=None, extKeys=None):
  """ Function dedicated to the StackedArea Chart

  https://www.tutorialspoint.com/python/time_strptime.htm
  """
  res = {}
  for key, vals in toMultiSeriesChart(recordSet, key, x, val, seriesNames, extKeys).items():
    res[key] = []
    for recordSet in vals:
      recordSet["bar"] = barStyle.get(recordSet["key"], False)
      recordSet["color"] = colors.get(recordSet["key"], False)
      res[key].append(recordSet)
  return res


# ------------------------------------------------------------------------------
# Bespoke Interface for the different charts
# ------------------------------------------------------------------------------
def toPlotBox(recordSet, keys, valCols, withMean=True, seriesNames=None):
  """ Transform a recordSet in a data Structure compatible with a Plot Box D3 item """
  q1Col, q2Col, q3Col, whisker_lowCol, whisker_highCol, outliersCol = valCols
  data = collections.defaultdict(lambda: collections.defaultdict(float))
  outliers = collections.defaultdict(list)
  keyAgg = keys[0][0]
  for rec in recordSet:
    data[rec[keyAgg]]['Q1'] += float(rec[q1Col])
    data[rec[keyAgg]]['Q2'] += float(rec[q2Col])
    data[rec[keyAgg]]['Q3'] += float(rec[q3Col])
    data[rec[keyAgg]]['whisker_low'] += float(rec[whisker_lowCol])
    data[rec[keyAgg]]['whisker_high'] += float(rec[whisker_highCol])
    data[rec[keyAgg]]['count'] += 1
    if outliersCol != '':
      outliers[keyAgg].append(rec[outliersCol])

  result = []
  names = {} if seriesNames is None else seriesNames
  if withMean:
    for key, vals in data.items():
      scaledVal = {}
      for itemKey, val in vals.items():
        if itemKey == 'count':
          continue

        scaledVal[itemKey] = val / vals['count']
      scaledVal['outliers'] = outliers[itemKey]
    result.append({'label': names.get(key, key), 'values': scaledVal})
  else:
    for key, vals in data.items():
      scaledVal = {}
      for itemKey, val in vals.items():
        if itemKey == 'count':
          continue
        scaledVal[itemKey] = val
      scaledVal['outliers'] = outliers[key]
    result.append({'label': names.get(key, key), 'values': scaledVal})
  return {'%s_FIXED' % keyAgg : result}

def toCandleStick(recordSet, dateInfo, openCol, highCol, lowCol, closeCol, volumeCol, adjustedCol):
  """  """
  res = []
  dateCol, dtFormat = dateInfo[0]
  for rec in recordSet:
    res.append({"date": rec[dateCol], "open": float(rec[openCol]), "high": float(rec[highCol]), "low": float(rec[lowCol]),
                "close": float(rec[closeCol]), "volume": float(rec[volumeCol]), "adjusted": float(rec[adjustedCol])})
  return {"%s_FIXED" % dateCol: [{'values': res}]}

def toSpider(recordSet, key, x, val, seriesNames=None, extKeys=None):
  """ """
  data = toMultiSeries(recordSet, key, x, val, seriesNames, extKeys)
  result = {}
  for key, vals in data.items():
    recordSet = {'keys': [], 'values': []}
    allCategories, sumPerKey, sumPerKeyPerCategory = set(), collections.defaultdict(float), collections.defaultdict(lambda: collections.defaultdict(float))
    for row in vals:
      recordSet['keys'].append(row['key'])
      #values = []
      for val in row['values']:
        #values.append({'axis': val[0], 'value': val[1]})
        allCategories.add(val[0])
        sumPerKey[row['key']] += abs(val[1])
        sumPerKeyPerCategory[row['key']][val[0]] += abs(val[1])

    recordSet = {'keys': sumPerKeyPerCategory.keys(), 'values': []}
    for subKeys in recordSet['keys']:
      values = []
      for category in allCategories:
        values.append({'axis': category, 'value': sumPerKeyPerCategory[subKeys][category] / sumPerKey[subKeys]})
      recordSet['values'].append(values)
      result[key] = recordSet

  return result

def toNetwork(recordSet, grpKeys):
  """ Return the data structure used for the Network - Force directed - chart """
  result = {}
  for keys in grpKeys:
    groups = collections.defaultdict(set)
    links = collections.defaultdict(set)
    for rec in recordSet:
      preVals = None
      for i, key in enumerate(keys):
        groups[i].add(rec[key])
        if preVals is not None:
          links["%s_%s" % (preVals, i-1)].add("%s_%s" % (rec[key], i))
        preVals = rec[key]

    nodes, j, mapLinks = [], 0, {}
    for i in range(len(keys)):
      for name in groups[i]:
        nodes.append({"name": name, "group": i},)
        mapLinks["%s_%s" % (name, i)] = j
        j += 1

    treeLinks = []
    for src, dsts in links.items():
      for dst in dsts:
        treeLinks.append({"source": mapLinks[src], "target": mapLinks[dst], "value": 1})
    result[regex.sub('', "_".join(keys))] = {'nodes': nodes, 'links': treeLinks}
  return result

# ------------------------------------------------------------------------------
# Interface for the tables
# ------------------------------------------------------------------------------
def toPivotTable(recordSet, keys, vals, removeZero=True, filters=None):
  """
  In order to produce a pivot table values should be float figures

  This is an version using basic python functions to allow users without Pandas to use it
  """
  parents = collections.defaultdict(lambda: collections.defaultdict(float))
  dimKeys = len(keys)
  if filters is not None:
    for rec in recordSet:
      for col, val in filters.items():
        if not rec[col] in val:
          break

      else:
        compositeKey = [''] * len(keys)
        for i, key in enumerate(keys):
          compositeKey[i] = str(rec[key])
          countVals = 0
          for j, val in enumerate(vals):
            if rec[val] == 0 and removeZero:
              continue

            countVals += 1
            parents[tuple(compositeKey)][val] += rec[val]
          if countVals > 0:
            parents[tuple(compositeKey)]['level'] = i
            parents[tuple(compositeKey)]['__count'] += 1
            if dimKeys == i+1:
              parents[tuple(compositeKey)]['_leaf'] = 1
  else:
    for rec in recordSet:
      compositeKey = [''] * len(keys)
      for i, key in enumerate(keys):
        compositeKey[i] = str(rec[key])
        countVals = 0
        for j, val in enumerate(vals):
          if rec[val] == 0 and removeZero:
            continue

          countVals += 1
          parents[tuple(compositeKey)][val] += rec[val]
        if countVals > 0:
          parents[tuple(compositeKey)]['level'] = i
          parents[tuple(compositeKey)]['__count'] += 1
          if dimKeys == i+1:
            parents[tuple(compositeKey)]['_leaf'] = 1
  fullKeys = sorted(parents.keys())
  result = []
  for compKey in fullKeys:
    row = dict(zip(keys, list(compKey)))
    for val in vals:
      row[val] = parents[compKey][val]
    comKeyClean = [regex.sub('', ''.join(comp).strip()) for comp in compKey]
    classCleanKey, prevKey = [], ''
    for i in range(0, len(comKeyClean)):
      prevKey = "%s%s" % (prevKey, comKeyClean[i])
      classCleanKey.append(prevKey)
    row['cssCls'] = list(set(classCleanKey)) # parents[compKey]['cssCls'][:-1]
    row['_id'] = "".join(comKeyClean[0:parents[compKey]['level']+1])
    if parents[compKey]['_leaf'] == 1:
      row['_leaf'] = 1
      row['_hasChildren'] = 0
    else:
      row['_leaf'] = 0
      row['_hasChildren'] = 1
    if parents[compKey]['level'] == 0:
      row['_parent'] = 1
      row['_leaf'] = 0
    else:
      for i in range(parents[compKey]['level']):
        row[keys[i]] = '' # Remove the duplicated entries
      row['_parent'] = 0
    row['level'] = parents[compKey]['level']
    result.append(row)
  return result

def toAggTable(recordSet, keys, vals, removeZero=True, filters=None):
  """

  """
  parents = collections.defaultdict(lambda: collections.defaultdict(float))
  if filters is not None:
    for rec in recordSet:
      for col, val in filters.items():
        if not rec[col] in val:
          break

      else:
        compositeKey = [rec[key] for key in keys]
        for j, val in enumerate(vals):
          if rec[val] == 0 and removeZero:
            continue

          parents[tuple(compositeKey)][val] += rec[val]
  else:
    for rec in recordSet:
      compositeKey = [rec[key] for key in keys]
      for j, val in enumerate(vals):
        if rec[val] == 0 and removeZero:
          continue

        parents[tuple(compositeKey)][val] += rec[val]
  fullKeys = sorted(parents.keys())
  result = []
  for compKey in fullKeys:
    row = dict(zip(keys, list(compKey)))
    for val in vals:
      row[val] = parents[compKey][val]
    comKeyClean = [regex.sub('', ''.join(comp).strip()) for comp in compKey]
    classCleanKey, prevKey = [], ''
    for i in range(0, len(comKeyClean)):
      prevKey = "%s%s" % (prevKey, comKeyClean[i])
      classCleanKey.append(prevKey)
    result.append(row)
  return result

def toVenn(recordSet, col1, col2, vals, extKeys=None):
  """
  Simple Venn chart based on two columns

  """
  tmpResults = collections.defaultdict(int)
  for rec in recordSet:
    if vals[0][1] is not None:
      tmpResults[(rec[col1], rec[col2])] += vals[0][1](rec[vals[0][0]])
      tmpResults[(rec[col1],)] += vals[0][1](rec[vals[0][0]])
      tmpResults[(rec[col2],)] += vals[0][1](rec[vals[0][0]])
    else:
      tmpResults[(rec[col1], rec[col2])] += rec[vals[0][0]]
      tmpResults[(rec[col1],)] += rec[vals[0][0]]
      tmpResults[(rec[col2],)] += rec[vals[0][0]]
  result = []
  for cat, value in tmpResults.items():
    result.append({'sets': cat, 'size': int(value)},)
  return {'%s_%s_%s' % (col1, col2, vals[0][0]): result}



if __name__ == '__main__':
  recordSet = [{'cpty': 'BNPPAR', 'ptf' : 11, 'prd': 'Trs', 'value': 10},
               {'cpty': 'BNPPAR', 'ptf' : 12, 'prd': 'Bond', 'value': 10},
               {'cpty': 'BNPPAR', 'ptf' : 12, 'prd': 'Cds', 'value': 10}]

  keys = [['cpty', 'ptf', 'prd']]
  vals = ['value']
  import json
  print( json.dumps(toVenn(recordSet, 'cpty', 'ptf', 'value')))
