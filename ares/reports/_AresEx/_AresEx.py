"""

"""


NAME = 'Ares Example'
# Just to set up the menu on the left hand side
SHORTCUTS = [('Text', [('Input Events', 'AresExText'),

                         ]),

              ('Tables', [('Basic Table', 'AresExTables'),
                         ('Complex Table', 'AresExTablesComplex'),
                         ('Ajax Table', 'AresExTableAjax'),
                         ('Table with Chart', 'AresExTablePie')
                         ]),
             ('Graphs', [('Basic Charts', 'AresExSimpleCharts'),
                         ('Other Charts', 'AresExMultiCharts'),
                         ('Multi Bar Charts', 'AresExMultiBarChart'),
                         ]),

             ('Templates', [
               ('Data Extraction', 'AresDataExtract'),
               ('Dashboard 1', 'AresDashboard1.py'),
                      ]),
              ]

def report(aresObj):
  """

  """
  aresObj.title("Ares from some examples")
