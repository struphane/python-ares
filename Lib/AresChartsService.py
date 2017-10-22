""" Service dedicated to convert your recordSet to an object that your graph will recognise
@author: Olivier Noguès

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


def toPie(recordSet, key, val):
  """ Function dedicated to the Pie Chart and the Donut chart

  """
  return json.dumps(to2DCharts(recordSet, None, key, val)[0]['values'])

def toBar(recordSet, seriesName, key, val):
  """ Function dedicated to the Bar Chart

  """
  return json.dumps(to2DCharts(recordSet, seriesName, key, val))