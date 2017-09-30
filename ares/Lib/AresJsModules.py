"""

"""

from flask import render_template_string

JS_IMPORTS = {
  'ares': {'modules': ['ares.js']},

  'bootstrap': {'modules': ['bootstrap.min.js']},

  # Javascript packages to handle DataTables
  'dataTables': {'req': ['jquery'],
                 'modules': ['jquery.dataTables.min.js', 'dataTables.buttons.min.js',
                             'dataTables.responsive.min.js', 'buttons.colVis.min.js']},

  # Jquery package
  'jquery': {'modules': ['jquery-3.2.1.min.js']},

  # Javascript packages for the PDF transformation
  'pdfmake': {'modules': ['pdfmake.min.js', 'vfs_fonts.js']},

  # Javascript dependencies for D3 and NVD2 components
  'd3': {'req': ['jquery'],
         'modules': ['d3.v3.js', 'nv.d3.js']},

  # Javascript modules for the Cloud graph object
  'cloud': {'req': ['jquery', 'd3'],
            'modules': ['colorbrewer.js', 'd3.layout.cloud.js']},

  # Internal javascript packages for Ares
  'ares': {'modules': ['ares.js']},

  }

CSS_IMPORTS = {
  'jquery-ui': {'modules': ['jquery-ui.css'],
                },

  'dataTables': {'modules': ['jquery.dataTables.min.css', 'responsive.dataTables.min.css', 'buttons.dataTables.min.css'],
                 },

  'bootstrap': {'modules': ['bootstrap.min.css', 'metro-bootstrap.min.css']},

  'font-awesome': {'modules': ['font-awesome.min.css']},

  'd3': {'modules': ['svg.css', 'nv.d3.css']},

  'ares': {'modules': ['bdi.css', 'bootstrap-simple-sidebar.css']}
  }

class ImportManager(object):
  """

  """

  def cssResolve(self, cssAliases):
    """ Return the list of CSS modules to add to the header """
    cssList = []
    for cssAlias in cssAliases:
      cssDefinition = CSS_IMPORTS[cssAlias]
      for css in cssDefinition['modules']:
        if 'url' in cssDefinition :
          # In this case we want to use a specific module not necessarily in the server
          # Flask will not be used to translate the URL automatically
          cssList.append('<link rel="stylesheet" href="%s/%s" type="text/css">' % (cssDefinition['url'], css))
        else:
          cssList.append('<link rel="stylesheet" href="{{ url_for(\'static\',filename=\'css/%s\') }}" type="text/css">' % css)
    return render_template_string("\n".join(cssList))

  def jsResolve(self, jsAliases):
    """ Return the list of Javascript modules to add to the header """
    jsList = []
    for jsAlias in jsAliases:
      jsDefinition = JS_IMPORTS[jsAlias]
      for js in jsDefinition['modules']:
        if 'url' in jsDefinition :
          # In this case we want to use a specific module not necessarily in the server
          # Flask will not be used to translate the URL automatically
          jsList.append('<script language="javascript" type="text/javascript" src="%s/%s"></script>' % (jsDefinition['url'], js))
        else:
          jsList.append('<script language="javascript" type="text/javascript" src="{{ url_for(\'static\',filename=\'js/%s\') }}"></script>' % js)
    return render_template_string("\n".join(jsList))

