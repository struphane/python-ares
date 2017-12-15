"""


"""


def report(aresObj):
  """

  :param aresObj:
  :return:
  """
  ptfRecordSets = [
    {'portfolio': 1111},
    {'portfolio': 2222},
    {'portfolio': 3333},
  ]

  ptfCpty = [
    {'portfolio': 1111, 'counterparty': 'AAAA', 'cpty_name': 'Counterparty A', 'grr': 40, 'entry_dt': '2017-01-01', 'provision': 0},
    {'portfolio': 1111, 'counterparty': 'BBBB', 'cpty_name': 'Counterparty B', 'grr': 30, 'entry_dt': '2017-06-01', 'provision': 300},
    {'portfolio': 1111, 'counterparty': 'BBBB', 'cpty_name': 'Counterparty B', 'grr': 30, 'entry_dt': '2017-06-01', 'provision': 300},
    {'portfolio': 1111, 'counterparty': 'CCCC', 'cpty_name': 'Counterparty C', 'grr': 50, 'entry_dt': '2017-03-01', 'provision': 0},

    {'portfolio': 2222, 'counterparty': 'CCCC', 'cpty_name': 'Counterparty C', 'grr': 50, 'entry_dt': '2017-03-01', 'provision': 0},
    {'portfolio': 2222, 'counterparty': 'DDDD', 'cpty_name': 'Counterparty D', 'grr': 40, 'entry_dt': '2016-01-01', 'provision': 0},
    {'portfolio': 2222, 'counterparty': 'EEEE', 'cpty_name': 'Counterparty E', 'grr': 60, 'entry_dt': '2016-01-01', 'provision': 0},
    {'portfolio': 2222, 'counterparty': 'FFFF', 'cpty_name': 'Counterparty F', 'grr': 90, 'entry_dt': '2016-01-01', 'provision': 0},

    {'portfolio': 3333, 'counterparty': 'FFFF', 'cpty_name': 'Counterparty F', 'grr': 90, 'entry_dt': '2016-01-01', 'provision': 0},
    {'portfolio': 3333, 'counterparty': 'GGGG', 'cpty_name': 'Counterparty G', 'grr': 40, 'entry_dt': '2017-03-01', 'provision': 0},
    {'portfolio': 3333, 'counterparty': 'HHHH', 'cpty_name': 'Counterparty H', 'grr': 40, 'entry_dt': '2017-03-01', 'provision': 0},
    {'portfolio': 3333, 'counterparty': 'IIII', 'cpty_name': 'Counterparty I', 'grr': 40, 'entry_dt': '2017-03-01', 'provision': 0},
    {'portfolio': 3333, 'counterparty': 'JJJJ', 'cpty_name': 'Counterparty J', 'grr': 40, 'entry_dt': '2017-02-01', 'provision': 0},
    {'portfolio': 3333, 'counterparty': 'KKKK', 'cpty_name': 'Counterparty K', 'grr': 40, 'entry_dt': '2017-01-01', 'provision': 0},

  ]

  recordSet = [
              {'date': "2011-11-14T16:17:54Z", 'quantity': 2, 'total': 190, 'tip': 100, 'type': "tab"},
              {'date': "2011-11-14T16:20:19Z", 'quantity': 2, 'total': 190, 'tip': 100, 'type': "tab"},
              {'date': "2011-11-14T16:28:54Z", 'quantity': 1, 'total': 300, 'tip': 200, 'type': "visa"},
              {'date': "2011-11-14T16:30:43Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
              {'date': "2011-11-14T16:48:46Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
              {'date': "2011-11-14T16:53:41Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
              {'date': "2011-11-14T16:58:03Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
              {'date': "2011-11-14T17:07:21Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
              {'date': "2011-11-14T17:22:59Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
              {'date': "2011-11-14T17:22:59Z", 'quantity': 3, 'total': 90, 'tip': 0, 'type': "tab"},
              {'date': "2011-11-14T16:54:06Z", 'quantity': 1, 'total': 100, 'tip': 0, 'type': "cash"},
              {'date': "2011-11-14T17:25:45Z", 'quantity': 2, 'total': 200, 'tip': 0, 'type': "cash"},
              {'date': "2011-11-14T17:29:52Z", 'quantity': 1, 'total': 200, 'tip': 100, 'type': "visa"}
            ]

  data = aresObj.crossFilterData(recordSet, [])
  groupVar = data.group('quantity', 'total')
  groupVar3 = data.group('type', 'total')
  groupVar2 = data.group('date', 'total')

  aresObj.title("Portfolio View")

  table = aresObj.table(ptfCpty,
                [{'colName': 'Portfolio', 'key': 'portfolio', 'dsc': 'Data extracted from CRDS'},
                 {'colName': 'Cpty Code', 'key': 'counterparty', 'dsc': 'Data extracted from CRDS'},
                 {'colName': 'Cpty Name', 'key': 'cpty_name', 'dsc': 'Data extracted from CRDS'},
                 {'colName': 'GRR', 'key': 'grr', 'dsc': 'Data from MRX'},
                 {'colName': 'Entry Date', 'key': 'entry_dt'},
                 {'colName': 'Provision', 'key': 'provision'},
                ]
                )
  table.callBackCreateUrl(1, 'ViewCpty')
  table.callBackCreateCellNumberUpDown(4, 0)
  table.callBackCreateProgressBar(3)

  pie = aresObj.xmeter(groupVar)
  pie.val(33)
  pie.showLegend(False)

  pie2 = aresObj.xdonut(groupVar3)
  pie2.showLegend(False)
  aresObj.row([table, aresObj.col([pie, pie2])])
  ptfXRec = aresObj.crossFilterData(ptfRecordSets, [])