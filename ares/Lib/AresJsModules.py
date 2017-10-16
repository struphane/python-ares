"""

"""

import collections
from flask import render_template_string

JS_IMPORTS = {
  # module are written from the first one to load to the last one
  'bootstrap': {'req': ['jquery'], 'modules': ['tether.min.js', 'bootstrap.min.js']},

  # Javascript packages to handle DataTables
  'dataTables': {'req': ['jquery', 'bootstrap'],
                 'modules': ['jquery.dataTables.min.js', 'dataTables.buttons.min.js',
                             'dataTables.responsive.min.js', 'buttons.colVis.min.js',
                             'dataTables.fixedColumns.min.js']},

  # Jquery package
  'jquery': {'modules': ['jquery-3.2.1.min.js', 'jquery-ui.min.js']},

  # Javascript packages for the PDF transformation
  'pdfmake': {'modules': ['pdfmake.min.js', 'vfs_fonts.js']},

  # Javascript dependencies for D3 and NVD2 components
  'd3': {'req': ['jquery', 'bootstrap'],
         'modules': ['d3.v3.min.js', 'nv.d3.min.js']},

  # Javascript modules for the Cloud graph object
  'cloud': {'req': ['d3'], 'modules': ['colorbrewer.js', 'd3.layout.cloud.js']},

  # Internal javascript packages for Ares
  'ares': {'req': ['bootstrap'], 'modules': ['ares.js']},

  # Cannot add properly the dependency in this one as my algorithm does not work for shared dependencies ....
  'meter': {'req': ['d3'], 'modules': ['d3.meter.js']},

  # Mapael library
  'raphael': {'req': ['jquery'], 'modules': ['raphael.min.js']},
  'mapael': {'req': ['jquery', 'raphael'], 'modules': ['jquery.mapael.min.js']},
  }

CSS_IMPORTS = {
  'jquery': {'modules': ['jquery-ui.css']},

  'dataTables': {'req': ['bootstrap'], 'modules': ['jquery.dataTables.min.css', 'responsive.dataTables.min.css',
                                                   'buttons.dataTables.min.css']},

  'bootstrap': {'req': ['font-awesome'], 'modules': ['bootstrap.min.css', 'metro-bootstrap.min.css']},

  'font-awesome': {'modules': ['font-awesome.min.css'],
                   #'url': 'https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css'
                   },

  'd3': {'req': ['bootstrap'], 'modules': ['nv.d3.min.css']},

  'ares': {'req': ['bootstrap'], 'modules': ['bdi.css', 'bootstrap-simple-sidebar.css']},
  }


class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

class ImportManager(object):
  """
  """
  def __init__(self):
    """ Load the hierarchy of modules """
    self.jsImports, self.cssImports = {}, {}
    for folder, importDic, importType in [('js', self.jsImports, JS_IMPORTS), ('css', self.cssImports, CSS_IMPORTS)]:
      for alias, definition in importType.items():
        main = OrderedSet()
        for mod in definition['modules']:
          if 'url' in definition:
            main.add("%s/%s" % (definition['url'], mod))
          else:
            main.add("{{ url_for(\'static\',filename=\'%s/%s\') }}" % (folder, mod))
        modules = OrderedSet()
        self.getModules(modules, alias, folder, importType)
        importDic[alias] = {'main': main, 'dep': modules}

  def getModules(self, modules, alias, folder, defModule):
    """ Return the list of modules for a given entry """
    for mod in defModule[alias]['modules']:
      if 'url' in defModule[alias]:
        modules.add("%s/%s" % (defModule[alias]['url'], mod))
      else:
        modules.add("{{ url_for(\'static\',filename=\'%s/%s\') }}" % (folder, mod))
    for req in defModule[alias].get('req', []):
      self.getModules(modules, req, folder, defModule)

  def getReq(self, mod, modList,importHierarchy ):
    modList.append(mod)
    for req in importHierarchy[mod].get("req", []):
      self.getReq(req, modList, importHierarchy)

  def cleanImports(self, imports, importHierarchy):
    """  Remove the underlying imports to avoid duplicated entries """
    importResolve = []
    for mod in imports:
      self.getReq(mod, importResolve, importHierarchy)
    setImport = set(importResolve)
    for a in setImport:
      occurences = [j for j, x in enumerate(importResolve) if x == a]
      if len(occurences) > 1:
        for j in occurences[::-1][1:]:
          importResolve.pop(j)
    return importResolve[::-1]

  def cssResolve(self, cssAliases):
    """ Return the list of CSS modules to add to the header """
    cssList = []
    cssAliases = self.cleanImports(cssAliases, CSS_IMPORTS)
    for cssAlias in cssAliases:
      for urlModule in list(self.cssImports[cssAlias]['main']):
        cssList.append('<link rel="stylesheet" href="%s" type="text/css">' % urlModule)
    return render_template_string("\n".join(cssList))

  def jsResolve(self, jsAliases):
    """ Return the list of Javascript modules to add to the header """
    jsList = []
    jsAliases = self.cleanImports(jsAliases, JS_IMPORTS)
    for jsAlias in jsAliases:
      for urlModule in list(self.jsImports[jsAlias]['main']):
        jsList.append('<script language="javascript" type="text/javascript" src="%s"></script>' % urlModule)
    return render_template_string("\n".join(jsList))

  def cssGetAll(self):
    """ To retrieve the full list of available modules on the server """
    return self.cssResolve(set(CSS_IMPORTS.keys()))

  def jsGetAll(self):
    """ To retrieve the full list of available modules on the server """
    return self.jsResolve(set(JS_IMPORTS.keys()))