"""

"""

jsImport = {
  'ares': 'ares.js',

  'bootstrap': 'bootstrap.min.js',

  # Javascript packages to handle DataTables
  'dataTables': {'req': ['jquery'],
                 'modules': ['jquery.dataTables.min.js', 'dataTables.buttons.min.js',
                             'dataTables.responsive.min.js', 'buttons.colVis.min.js']},

  # Jquery package
  'jquery': 'jquery-3.2.1.min.js',

  # Javascript packages for the PDF transformation
  'pdfmake': ['pdfmake.min.js', 'vfs_fonts.js'],

  # Javascript dependencies for D3 and NVD2 components
  'd3': {'req': ['jquery'],
         'modules': ['d3.v3.js', 'nv.d3.js']},

  # Javascript modules for the Cloud graph object
  'cloud': {'req': ['jquery', 'd3'],
            'modules': ['colorbrewer.js', 'd3.layout.cloud.js']},

  # Internal javascript packages for Ares
  'ares': {'modules': ['ares.js']},

  }

cssImport = {
  'jquery-ui': {'modules': ['jquery-ui.css'],
                'url': '',
                },

  'dataTables': {'modules': ['jquery.dataTables.min.css', 'responsive.dataTables.min.css', 'buttons.dataTables.min.css']},

  'bootstrap': {'modules': ['bootstrap.min.css', 'metro-bootstrap.min.css']},

  'font-awesome': {'modules': 'font-awesome.min.css'},

  'd3': {'modules': ['svg.css', 'nv.d3.css']},

  'ares': {'modules': ['bdi.css', 'bootstrap-simple-sidebar.css']}
  }

class ImportManager(object):
  """

  """

