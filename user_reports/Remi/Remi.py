import random

NAME = "Remi Test Report"

def getMrxData(config, dynamicLst=[]):
  ptfLst = ["1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576"]
  product = ["Vanilla Swap", "Exotic Option", "Future", "Option", "Bond"]
  return [{}]

def getData():
  cptyLst = ["BNPPAR", "SOCGEN", "BARCLON", "JPMORG", "MORGSTAN", "DEUTBAN", "CRDSUISS"]
  rtgLst = range(1, 18)
  ctyLst = ["US", "CA", "GB", "FR", "DE", "IT", "JP"]
  ptfLst = [1024, 2048, 4096]

  return [{"cpty_cod": cpty, "rtg":rtg, "iss_cty": cty, "ptf_cod": ptf
          , "deal_cod": "%s%s" % (cty, random.randint(100000000000, 999999999999))
          , "pv": random.random()*random.choice([-10000, 10000]), "exposure": random.random()*random.choice([-10000, 10000])}
              for cpty in cptyLst
              for rtg in rtgLst
              for cty in ctyLst
              for ptf in ptfLst
              for _ in range(2)][:5]

def report(aresObj):
  data = getData()

  table = aresObj.tablepivot( data
                       , [ {"colName": "Counterparty", "key": "cpty_cod"}
                         , {"colName": "Rating", "key": "rtg"}
                         , {"colName": "Iss Cty", "key": "iss_cty"}
                         , {"colName": "Portfolio", "key": "ptf_cod"}
                         , {"colName": "Deal", "key": "deal_cod"}
                         , {"colName": "PV", "key": "pv"}
                         , {"colName": "Expo", "key": "exposure"}
                         ]
                       , headerBox="Data"
                       )
  table.setCols(["cpty_cod"])
  table.setRows(["rtg", "ptf_cod"])
  table.setRendererName("Heatmap")
  #table.setAggFun(("Sum over Sum", ["pv", "exposure"]))
  #table.setAggFun(("Count Unique", ["pv"]))
  table.setAggFun(("Diff Abs", ["pv", "exposure"]))

  #table.pivot(["cpty_cod", "rtg"], ["pv", "exposure"])
  #aresObj.table([], [])
  aresObj.table(data, [{"colName": "Counterparty", "key": "cpty_cod"}], headerBox="Table Test")

