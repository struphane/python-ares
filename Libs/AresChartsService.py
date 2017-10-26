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
import json
import time
import datetime
import collections

regex = re.compile('[^a-zA-Z0-9]')

def to2DCharts(recordSet, seriesName, keysWithFormat, valsWithFormat):
  """ Function dedicated to return from a recordSet for the 2D charts with single series

  The key and val should be some keys defined in the recordSet.
  The values should be float data and the seriesName should be the name that you would like to display in your chart
  """
  data = collections.defaultdict(lambda: collections.defaultdict(float))
  trsnsfValFormat = []
  for val, valFormat in valsWithFormat:
    if valFormat is None:
      trsnsfValFormat.append((val, float))
    else:
      trsnsfValFormat.append((val, {'int': int, 'float': float, 'number': float}[valFormat]))
  for key, format in keysWithFormat:
    if format is not None: # If there is a timestamp format defined
      mapFnc = lambda dt, dtFmt: int(datetime.datetime.strptime(dt, dtFmt).timestamp())
    else:
      mapFnc = lambda dt, dtFmt: str(dt)
    for rec in recordSet:
      for val, valFormat in trsnsfValFormat:
        data[(key, val)][mapFnc(rec[key], format)] += valFormat(rec[val])

  resultSets = {}
  for key, aggVals in data.items():
    result = [{'key': seriesName, 'values': []}]
    sortedDt = sorted(aggVals.keys())
    for dataKey in sortedDt:
      result[0]['values'].append([dataKey, aggVals[dataKey]])
    resultSets["_".join(key)] = result
  return resultSets

def toMultiSeriesChart(recordSet, keysWithFormat, xWithFormat, valsWithFormat, seriesNames=None):
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
    mapFnc = lambda dt, dtFmt: int(time.mktime(datetime.datetime.strptime(dt, dtFmt).timetuple()))
  else:
    mapFnc = lambda dt, dtFmt: str(dt)

  trsnsfValFormat = []
  for val, valFormat in valsWithFormat:
    if valFormat is None:
      trsnsfValFormat.append((val, float))
    else:
      trsnsfValFormat.append((val, {'int': int, 'float': float, 'number': float}[valFormat]))

  # Define the temporary dataSet used to aggregate the data in the recordSet
  data = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
  # Aggregate the data in the recordSet
  for key, keyFormat in keysWithFormat:
    for rec in recordSet:
      dt = mapFnc(rec[xWithFormat[0]], xWithFormat[1]) # Use the map function
      for val, valFormat in trsnsfValFormat:
        data[(key, val)][rec[key]][dt] += valFormat(rec[val])
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
  return resultSets


# ------------------------------------------------------------------------------
# Interface for the different charts
# ------------------------------------------------------------------------------
def toPie(recordSet, key, val):
  """ Function dedicated to the Pie Chart and the Donut chart

  """
  data = dict([(key, result[0]['values']) for key, result in to2DCharts(recordSet, None, key, val).items()])
  return data

def toBar(recordSet, seriesName, key, val):
  """ Function dedicated to the Bar Chart

  """
  return to2DCharts(recordSet, seriesName, key, val)

def toMultiSeries(recordSet, key, x, val, seriesNames=None):
  """ Function dedicated to the StackedArea Chart

  https://www.tutorialspoint.com/python/time_strptime.htm
  """
  return toMultiSeriesChart(recordSet, key, x, val, seriesNames)

def toComboChart(recordSet, key, x, val, seriesNames=None, barStyle=None, colors=None):
  """ Function dedicated to the StackedArea Chart

  https://www.tutorialspoint.com/python/time_strptime.htm
  """
  res = {}
  for key, vals in toMultiSeriesChart(recordSet, key, x, val, seriesNames).items():
    res[key] = []
    for recordSet in vals:
      recordSet["bar"] = barStyle.get(recordSet["key"], False)
      recordSet["color"] = colors.get(recordSet["key"], False)
      res[key].append(recordSet)
  return res

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

def toHyrTable(recordSet, keys, vals):
  """
  In order to produce a pivot table values should be float figures

  This is an version using basic python functions to allow users without Pandas to use it
  """
  parents = collections.defaultdict(lambda: collections.defaultdict(float))
  for rec in recordSet:
    compositeKey = [''] * len(keys)
    #cssClass = []
    for i, key in enumerate(keys):
      compositeKey[i] = rec[key]
      for j, val in enumerate(vals):
        parents[tuple(compositeKey)][val] += rec[val]
      #cssClass.append(regex.sub('', ''.join(compositeKey).strip()))
      parents[tuple(compositeKey)]['level'] = i
      #parents[tuple(compositeKey)]['cssCls'] = list(cssClass)
      parents[tuple(compositeKey)]['__count'] += 1
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
    if parents[compKey]['__count'] == 1:
      row['_leaf'] = 1
    else:
      row['_hasChildren'] = 1
    if parents[compKey]['level'] == 0:
      row['_parent'] = 1
    row['level'] = parents[compKey]['level']
    result.append(row)
  return result
