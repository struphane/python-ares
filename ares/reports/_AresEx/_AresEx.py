"""

"""


NAME = 'Ares Example'
# Just to set up the menu on the left hand side
SHORTCUTS = [('Tables', [('Basic Table', 'AresExTables'),
                         ('Complex Table', 'AresExTablesComplex'),
                         ('Ajax Table', 'AresExTableAjax'),
                         ('Table with Chart', 'AresExTablePie')
                         ]),
             ('Graphs', [('Basic Graphs', 'AresExCharts'),

                         ]),

             ('Templates', [('Data Extraction', 'AresDataExtract'),
                      ]),
              ]

def report(aresObj):
  """

  """
  aresObj.title("Ares from some examples")
