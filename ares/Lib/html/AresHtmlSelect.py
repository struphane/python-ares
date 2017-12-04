""" Python wrapper for the HTML Select object
@author: Olivier Nogues

"""

import json

from ares.Lib import AresHtml
from ares.Lib import AresItem
from flask import render_template_string


class SelectDropDown(AresHtml.Html):
  """

  """
  alias, cssCls = 'dropdown', ['btn', 'btn-success']
  references = ['http://getbootstrap.com/docs/4.0/components/dropdowns/']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, title, vals, cssCls=None, cssAttr=None):
    """ Instantiate the Drop Down button """
    super(SelectDropDown, self).__init__(aresObj, list(vals), cssCls, cssAttr)
    self.title = title
    self.disableItems = {}
    # To replace non alphanumeric characters https://stackoverflow.com/questions/20864893/javascript-replace-all-non-alpha-numeric-characters-new-lines-and-multiple-whi
    self.jsFrg = ["%s = $(this).text().trim().replace(/\W+/g, '');" % self.htmlId]
    self.allowTableFilter = []

  def setDefault(self, value):
    """ Set a selected default value """
    self.aresObj.jsGlobal.add("%s = '%s';" % (self.htmlId, value))

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return self.htmlId

  def addCategory(self, items, level, vals):
    """ Add recursively the sub categories """
    for value, hyperlink in vals:
      if value is None:
        # Special keywork to put a delimiter
        # or a header if the hyperlink information is not None
        if hyperlink is not None:
          items.add(level, '<h6 class="dropdown-header">%s</h6>' % hyperlink)
        else:
          items.add(level, '<div class="dropdown-divider"></div>')
        continue

      if isinstance(hyperlink, list):
        items.add(level, '<li class="dropdown-submenu">')
        items.add(level, '<a href="#" class="dropdown-toggle dropdown-item" data-toggle="dropdown">%s</a>' % value)
        items.add(level, '<ul class="dropdown-menu">')
        self.addCategory(items, level+1, hyperlink)
        items.add(level, '</ul></li>')
      else:
        hyperLinkVal = hyperlink if hyperlink is not None else '#'
        if (hyperlink, value) in self.disableItems:
          items.add(level, '<li><a class="dropdown-item disabled" href="%s">%s</a></li>' % (hyperLinkVal, value))
        else:
          items.add(level, '<li><a class="dropdown-item" href="%s">%s</a></li>' % (hyperLinkVal, value))

  def disable(self, value, hyperlink):
    """ Disable an item from the dropdown box """
    self.disableItems[(hyperlink, value)] = True

  @property
  def jqId(self):
    """
    Property to get the Jquery ID of a python HTML object
    The use of ' instead of " is because the dumps will add some \ and it will not be correctly taken into account
    by the javascript layer
    """
    return "$('#%s > li a').not('.drilldown, .disabled')" % self.htmlId

  def __str__(self):
    """  String representation of a Drop Down item """
    items = AresItem.Item('<div class="dropdown">')
    items.add(1, '<button class="%s" type="button" data-toggle="dropdown">%s' % (self.getClass(), self.title))
    items.add(3, '<span class="caret"></span>')
    items.add(2, '</button>')
    items.add(1, '<ul class="dropdown-menu" id="%s">' % self.htmlId)
    self.addCategory(items, 2, self.vals)
    items.add(1, "</ul>")
    items.add(0, "</div>")
    self.aresObj.jsGlobal.add("%s_allow_tables = %s" % (self.htmlId, json.dumps(self.allowTableFilter)) )
    return str(items)

  def link(self, jsEvent):
    """ Change the component to use javascript functions """
    jsFrg = list(self.jsFrg)
    jsFrg.append(jsEvent)
    self.js('click', ";".join(jsFrg))


class SelectDropDownAjax(SelectDropDown):
  """
  This object will allow you to interact with the data and to request new set of data.
  This will not work locally, in order to get something locally you need to change your object to be a
  simple SelectDropDown


  """
  alias, cssCls = 'ajaxDropdown', ['btn', 'btn-success']
  references = ['http://getbootstrap.com/docs/4.0/components/dropdowns/']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def targetScript(self, script):
    self.script = script

  def click(self, htmlObjects):
    """ Call the ajax service and update the corresponding objects on the page """
    url = render_template_string("{{ url_for( 'ares.ajaxCall', report_name='%s', script='%s' ) }}" % (self.aresObj.http["REPORT_NAME"], self.script))
    self.js('click', '''$.ajax({url: '%s',
          success: function(result){var resultObj = JSON.parse(result);$('#%s').html(resultObj['data']); }});''' % (url, htmlObjects[0].htmlId))


class Select(AresHtml.Html):
  """
  Basic wrapper to the Select HTML Tag
    https://silviomoreto.github.io/bootstrap-select/examples/

  For example to get a change on the Select Box Item in the
  Javascript call back method
    - alert($(this).val()) ;

  For example
    [('Fruit', ['Apple', 'Banana'])]

  Default class parameters
  cssCls = selectpicker
  """
  # TODO: Extend the python object to handle multi select and all the cool features
  alias, cssCls = 'select', ['form-control']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, recordSet, title, col=None, cssCls=None, cssAttr=None, selected=None):
    """ Instantiate the object and store the selected item """
    if col is not None:
      vals = set([])
      for rec in recordSet:
        if col in rec:
          vals.add(rec[col])
    else:
      vals = set(recordSet)
    super(Select, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.title = title
    self.selected = selected

  def __str__(self):
    """ Return the HTML string for a select """
    item = AresItem.Item('<div class="form-group">', self.incIndent)
    item.add(1, '<label for="sel1">%s:</label>' % self.title)
    item.add(1, '<select %s>' % self.strAttr())
    for val in self.vals:
      if val == self.selected:
        item.add(3, '<option value="%s" selected>%s</option>' % (val, val))
      else:
        item.add(3, '<option value="%s">%s</option>' % (val, val))
    item.add(1, '</select>')
    item.add(0, '</div>')
    return str(item)

  def link(self, jsEvent):
    """ Change the component to use javascript functions """
    jsFrg = list(self.jsFrg)
    jsFrg.append(jsEvent)
    self.js('change', ";".join(jsFrg))

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return "$('#%s option:checked').val()" % self.htmlId

  def change(self, fnc):
    self.aresObj.jsOnLoadFnc.add('''
      $('#%(htmlId)s').on('change', function (event){ %(fnc)s }) ''' % {'htmlId': self.htmlId, 'fnc': fnc} )

  def update(self, dicKeys=None, htmlObjs=None, effects=None):
    """ """
    data = dicKeys.get(self.val) if dicKeys is not None else ''
    jsEffects = effects if effects is not None else []
    objUpdate = []
    if htmlObjs is not None:
      for htmlObj in htmlObjs:
        objUpdate.append(htmlObj.jsUpdate(data))
    self.aresObj.jsOnLoadFnc.add('''
      $('#%(htmlId)s').on('change', function (event){ %(objUpdt)s ; %(jsEffects)s ;}) ;
      ''' % {'htmlId': self.htmlId, 'data': data, 'objUpdt': '; '.join(objUpdate), 'jsEffects': ';'.join(jsEffects)})


class SelectWithGroup(AresHtml.Html):
  """
  Basic wrapper to the Select HTML Tag
    https://silviomoreto.github.io/bootstrap-select/examples/

  For example to get a change on the Select Box Item in the
  Javascript call back method
    - alert($(this).val()) ;

  For example
    [('Fruit', ['Apple', 'Banana'])]

  Default class parameters
  cssCls = selectpicker
  """
  # TODO: Extend the python object to handle multi select and all the cool features
  alias, cssCls = 'select_group', ['selectpicker']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

  def __str__(self):
    """ Return the HTML string for a select """
    item = AresItem.Item('<select %s>' % self.strAttr(), self.incIndent)
    for group, vals in self.vals:
      item.add(1, '<optgroup label="%s">' % group)
      for v in vals:
        item.add(2, '<option>%s</option>' % v)
      item.add(1, '</optgroup>')
    item.add(0, '</select>')
    return str(item)


class SelectMulti(AresHtml.Html):
  """ """
  alias, cssCls = 'select', []
  reqCss = ['multiselect']
  reqJs = ['multiselect']

  def __init__(self, aresObj, title, vals, cssCls=None, cssAttr=None):
    """ Instantiate the Drop Down button """
    super(SelectMulti, self).__init__(aresObj, list(vals), cssCls, cssAttr)
    self.title = title
    self.disableItems = {}
    self.aresObj.jsOnLoadFnc.add('%s.multiselect();' % self.jqId)
    self.allowTableFilter = []

  def selected(self, vals):
    """ Set default selected values """
    self.aresObj.jsOnLoadFnc.add("%s.val(%s); %s.multiselect('refresh');" % (self.jqId, json.dumps(vals), self.jqId))

  def __str__(self):
    """ Return the HTML string for a select """
    item = AresItem.Item('<select %s multiple="multiple">' % self.strAttr(), self.incIndent)
    for group, vals in self.vals:
      item.add(1, '<optgroup label="%s">' % group)
      for v in vals:
        item.add(2, '<option>%s</option>' % v)
      item.add(1, '</optgroup>')
    item.add(0, '</select>')
    return str(item)

  def click(self):
    """ Event on click """
    self.aresObj.jsOnLoadFnc.add(
     '''
        $('#%s').change(function(e) {
            alert('');
        });
     ''' % self.htmlId
    )
