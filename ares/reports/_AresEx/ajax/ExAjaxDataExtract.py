"""

"""


import ExAjaxRec


def call(aresObj):
  """
  """

  aresObj.setOutput('BasicExtract', "%s_%s_1.txt" % (aresObj.http['COB'], aresObj.http['NODE']))
  file = aresObj.setOutput('BasicExtract', "%s_%s_2.txt" % (aresObj.http['COB'], aresObj.http['NODE']))
  return {"status": "Updated", "data": aresObj.getOutputFrom("BasicExtract"), "content": ""}