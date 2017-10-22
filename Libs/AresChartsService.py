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

import json
import datetime
import collections

def to2DCharts(recordSet, seriesName, key, val):
  """ Function dedicated to return from a recordSet for the 2D charts with single series

  The key and val should be some keys defined in the recordSet.
  The values should be float data and the seriesName should be the name that you would like to display in your chart
  """
  data = collections.defaultdict(float)
  for rec in recordSet:
    data[rec[key]] += float(rec[val])
  result = [{'key': seriesName, 'values': []}]
  for key, aggVal in data.items():
    result[0]['values'].append([key, aggVal])
  return result

def toMultiSeriesChart(recordSet, key, x, val, seriesNames=None, isXDt=None):
  """ Function dedicated to handle charts with multiple series

  In those chart each series will have a certain numboer of points and the series name might be defined.
  Basically the x will be the series x abscisse, it will correspond to a key in the recordset and it can be
  converted to a timestamp if a isXDt format is defined. By default we will keep the value defined in the recordset
  Please have a look at the different keys possible:

  For example 2017-10-20 will be defined with a format %Y-%m-%d
  https://www.tutorialspoint.com/python/time_strptime.htm

  The special mapping table seriesNames, will allow to define propername for the series keys possible in the
  recordset
  """

  # Define the temporary dataSet used to aggregate the data in the recordSet
  data = collections.defaultdict(lambda: collections.defaultdict(int))
  if isXDt is not None: # If there is a timestamp format defined
    mapFnc = lambda dt, dtFmt: int(datetime.datetime.strptime(dt, dtFmt).timestamp())
  else:
    mapFnc = lambda dt, dtFmt: str(dt)
  # Aggregate the data in the recordSet
  for rec in recordSet:
    dt = mapFnc(rec[x], isXDt) # Use the map function
    data[rec[key]][dt] += float(rec[val])
  # Produce the final data structure required by the multi series charts
  result = []
  for key, series in data.items():
    seriesData = {'key': seriesNames.get(key, key) if seriesNames is not None else key, 'values': []}
    sortedDt = sorted(series.keys())
    for dt in sortedDt:
      seriesData['values'].append([dt, series[dt]])
    result.append(seriesData)
  return result


# ------------------------------------------------------------------------------
# Interface for the different charts
# ------------------------------------------------------------------------------
def toPie(recordSet, key, val):
  """ Function dedicated to the Pie Chart and the Donut chart

  """
  return json.dumps(to2DCharts(recordSet, None, key, val)[0]['values'])

def toBar(recordSet, seriesName, key, val):
  """ Function dedicated to the Bar Chart

  """
  return json.dumps(to2DCharts(recordSet, seriesName, key, val))

def toMultiSeries(recordSet, key, x, val, seriesNames=None, isXDt=None):
  """ Function dedicated to the StackedArea Chart

  https://www.tutorialspoint.com/python/time_strptime.htm
  """
  return json.dumps(toMultiSeriesChart(recordSet, key, x, val, seriesNames, isXDt))

