"""

"""


import ExAjaxRec


def call(aresObj):
  """
  """

  aresObj.wData('BasicExtract', "%s_%s_1.txt" % (aresObj.http['COB'], aresObj.http['NODE']))
  file = aresObj.rData('BasicExtract', "%s_%s_2.txt" % (aresObj.http['COB'], aresObj.http['NODE']))
  return aresObj.listDataFrom("BasicExtract")