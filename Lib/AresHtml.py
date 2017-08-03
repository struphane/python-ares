""" Main module for the HTML wrappers

The htmlId is generated by the report layer to ensure that there is no overlap between the ID
This will also help on having comprehensive ID

Please make sure that all the CSS information are defined in a CSS class

"""

import Lib.AresJs as AresJs

INDENT = '  '

class HtmlItem(object):
  """
  Main Abstract class for the Html objects

  Alias will be used by the Ares Report Interface to map the name to the class.
  This alias will also be used in the HTML ID

  """
  alias = None
  jsEvent = None

  def __init__(self, htmlId, cssCls=None):
    """ Get the html object ID and store the CSS Class if passed """
    self.__htmlId = htmlId
    self.cssCls = cssCls

  @property
  def htmlId(self):
    if self.alias is not None:
      return "%s_%s" % (self.alias, self.__htmlId)

    return self.__htmlId

  def html(self, localPath):
    """
    """
    raise NotImplementedError('subclasses must override html()!')

  def js(self, evenType, jsDef):
    """
    Common implementation to add javascript callback functions

    This javascript wrapper include on purpose a defined set of javascript methods in order to control the calls
    If some Ajax / DB calls are required, users will have to directly defined those items when they are writing
    the python report
    """
    if not evenType in getattr(self, 'jQueryEvent', []):
      # This is a check to control the number of events per class
      # Also because some of them might require specific display
      print('Do not use any Ajax call or bespoke methods here')
      print('In the function is not implemented yet please have a look at the call in AreHtml.py')
      raise Exception('%s not defined for this %s!' % (evenType, self.__class__))

    if self.jsEvent is None:
      self.jsEvent = [(evenType, jsDef)]
    else:
      self.jsEvent.append((evenType, jsDef))

  def jsAjax(self, evenType, jsDef, scriptName, localPath, data=None, url=None):
    """
    """
    ajaxObject = AresJs.XsCallHtml(scriptName)
    if url is not None:
      ajaxObject.url = url
    ajaxObject.success(jsDef)
    vals = []
    for key, val in data.items():
      vals.append('"%s": %s' % (key, val))
    vals = '{%s}' % ",".join(vals)
    print (vals)
    if localPath is not None:
      self.js(evenType, ajaxObject.ajaxLocal(vals))
    else:
      self.js(evenType, ajaxObject.ajax(vals))

  def jsVal(self):
    """ Return the Javascript Value """
    return '%s.val()' % self.jsRef()

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    if self.alias is None:
      raise Exception('No valid Alias defined for %s!' % self.__class__)

    return '$("#%s")' % self.htmlId

  def jsOnLoad(self):
    """ Functions which need to be run in the header """
    pass


class Table(HtmlItem):
  """ Wrapper for the HTML table

  the cssCls class will be added to the table.
  If some style is needed at row or column level this has to be done in the CSS Style sheet.
  """
  headers = None
  vals = None
  alias = 'table'

  def __init__(self, htmlId, cols, values, cssCls=None):
    """ Set the content of the table """
    super(Table, self).__init__(htmlId) # To get the HTML Id
    self.headers = cols
    self.vals = values

  def html(self, localPath):
    """ Return the HTML object for the table """
    item = ['<table class="table">']
    item.append('%s<thead><tr>' % INDENT)
    for header in self.headers:
      item.append('%s%s<th>%s</th>' % (INDENT, INDENT, header))
    item.append('%s</tr></thead>' % INDENT)
    for row in self.vals:
      item.append("%s<tr>" % INDENT)
      for val in row:
        item.append("%s%s<td>%s</td>" % (INDENT, INDENT, val))
      item.append("%s</tr>" % INDENT)
    item.append('</table>')
    return "\n".join(item)

class List(HtmlItem):
  """

  """
  val = None
  alias = 'list'
  def __init__(self, htmlId, values):
    """
    """
    super(List, self).__init__(htmlId) # To get the HTML Id
    self.val = values

  def html(self, localPath):
    """
    """
    item = ['<ul class="list-group">']
    for label, cnt in self.val:
      item.append('%s<li class="list-group-item">%s<span class="badge">%s</span></li>' % (INDENT, label, cnt))
    item.append('</ul>')
    return "\n".join(item)

class DropDown(HtmlItem):
  """ Wrapper for a Dropdowm HTML object

  """
  val = None
  title = None
  jQueryEvent = ['click']
  alias = 'dropDown'

  def __init__(self, htmlId, title, values):
    """
    """
    super(DropDown, self).__init__(htmlId) # To get the HTML Id
    self.val = values
    self.title = title # The default value

  def html(self, localPath):
    """
    """
    item = ['<div class="dropdown" id="%s">' % self.htmlId]
    item.append('<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">%s<span class="caret"></span></button>' % self.title)
    item.append('<ul class="dropdown-menu">')
    for val in self.val:
      item.append('%s<li><a href="#%s">%s</a></li>' % (INDENT, val[0], val[1]))
    item.append('</ul>')
    item.append('</div>')
    return "\n".join(item)

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object

    For example to get the selected item from a javascript call back function
      - alert($(this).text())

    """
    return '$("#%s .dropdown-menu li")' % self.htmlId

class Select(HtmlItem):
  """
  Basic wrapper to the Select HTML Tag

    https://silviomoreto.github.io/bootstrap-select/examples/

  For example to get a change on the Select Box Item in the Javascript call back method
    - alert($(this).val()) ;

  TODO: Extend the python object to handle multi select and all the cool features
  """

  val = None
  jQueryEvent = ['click', 'change']
  alias = 'select'

  def __init__(self, htmlId, values):
    """
    Values should be list of tuple and the tuple should be a label and a list
    for example:
      [('Nodes', ['GBC', 'BNPPAR']), ]
    """
    super(Select, self).__init__(htmlId) # To get the HTML Id
    self.val = values

  def html(self, localPath):
    """
    """
    item = ['<select class="selectpicker" id="%s">' % self.htmlId]
    for group, vals in self.val:
      item.append('%s<optgroup label="%s">' % (INDENT, group))
      for v in vals:
        item.append('%s%s<option>%s</option>' % (INDENT, INDENT, v))
      item.append('%s</optgroup>' % INDENT)
    item.append('</select>')
    return "\n".join(item)


class Div(HtmlItem):
  """ Wrapper for a simple DIV tag

  """
  val = None
  cls = None
  jQueryEvent = ['drop']
  alias = 'div'

  def __init__(self, htmlId, value, cssCls=None):
    """ Set the div value """
    super(Div, self).__init__(htmlId) # To get the HTML Id
    self.val = value
    self.cls = cssCls

  def html(self, localPath):
    """ Return the HMTL object of for div """
    if self.cls is not None:
      return '<div id="%s" class="%s">%s</div>' % (self.htmlId, self.cls, self.val)

    return '<div id="%s">%s</div>' % (self.htmlId, self.val)

  def JsVal(self):
    """ Return the Javascript Value """
    return '$("#%s").html()' % self.htmlId

class Container(Div):
  """ Wrapper for a simple DIV container

  """
  cls = 'container'
  htmlObjs = None
  alias = 'container'

  def __init__(self, htmlId, htmlObjs, cssCls=None):
    """ Set the div value """
    super(Div, self).__init__(htmlId) # To get the HTML Id
    self.htmlObjs = htmlObjs
    if cssCls is not None:
      self.cls = cssCls

  def html(self, localPath):
    """ Return the HMTL object of for div """
    self.val = "\n".join([htmlObj.html(localPath) for htmlObj in self.htmlObjs])
    return super(Container, self).html(localPath)

class Split(Div):
  """ Wrapper for a bootstrap Grid
  """
  cls = "container-fluid"
  htmlObjs = None
  alias = 'grid'

  def __init__(self, htmlId, htmlObjLeft, htmlObjRight, cssCls=None):
    """ Set the div value """
    super(Div, self).__init__(htmlId) # To get the HTML Id
    self.htmlObjs = [htmlObjLeft, htmlObjRight]
    if cssCls is not None:
      self.cls = cssCls

  def html(self, localPath):
    """ """
    res = ['<div id="%s" class="%s">' % (self.htmlId, self.cls)]
    res.append('%s<div class="row">' % INDENT)
    for htmObj in self.htmlObjs:
      res.append('%s%s<div class="col-lg-6">' % (INDENT, INDENT))
      res.append('%s%s%s' % (INDENT, INDENT, htmObj.html(localPath)))
      res.append('%s%s</div>' % (INDENT, INDENT))
    res.append('%s</div>' % INDENT)
    res.append('</div>')
    return "\n".join(res)

class Graph(HtmlItem):
  """ Wrapper to create a graph container """
  dim = None
  cssCls = 'span4'

  def __init__(self, htmlId, width, height, withSvg=True, cssCls=None):
    """ Store the HTML object dimension """
    super(Graph, self).__init__(htmlId) # To get the HTML Id
    self.dim = (width, height)
    self.withSvg = withSvg
    if cssCls is not None:
      self.cssCls = cssCls

  def html(self, localPath):
    """ Return the Graph container for D3 and DVD3 """
    if self.withSvg:
      return '<div id="chart%s" class="%s">\n<svg width="%s" height="%s"></svg>\n</div>\n' % (self.htmlId, self.cssCls, self.dim[0], self.dim[1])

    return '<div id="chart%s" class="%s"></div>\n' % (self.htmlId, self.cssCls)

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    if self.withSvg:
      return '$("#chart%s svg")' % self.htmlId

    return '$("#chart%s")' % self.htmlId

class NestedTable(Table):
  """
  This is a table of potential other HTML items

  This is not an optimised version of a table and it might be better to use dedicated bespoke new HTML classes
  if the needs are very specific.
  """
  alias = 'nestedtable'

  def html(self, localPath):
    """ Return the HTML object for the table """
    item = ['<table class="table">']
    item.append('%s<thead><tr>' % INDENT)
    for header in self.headers:
      item.append('%s%s<th>%s</th>' % (INDENT, INDENT, header))
    item.append('%s</tr></thead>' % INDENT)
    for row in self.vals:
      item.append("%s<tr>" % INDENT)
      for val in row:
        htmlStr = val.html(localPath) if hasattr(val, 'html') else val
        item.append("%s%s<td>%s</td>" % (INDENT, INDENT, htmlStr))
      item.append("%s</tr>" % INDENT)
    item.append('</table>')
    return "\n".join(item)


class Button(HtmlItem):
  """

  """
  val = None
  cssCls = None
  jQueryEvent = ['click']
  alias = 'button'

  def __init__(self, htmlId, value, cssCls=None):
    """
    """
    super(Button, self).__init__(htmlId) # To get the HTML Id
    self.val = value
    self.cssCls = cssCls

  def html(self, localPath):
    """
    """
    if self.cssCls is not None:
      return '<button id="%s" type="button" class="btn %s">%s</button>' % (self.htmlId, self.cssCls, self.val)

    return '<button id="%s" type="button" class="btn">%s</button>' % (self.htmlId, self.val)

class ButtonRemove(HtmlItem):
  """

  http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html
  """
  alias = 'remove'
  btype = 'danger'

  def __init__(self, htmlId, cssCls=None):
    """ """
    super(ButtonRemove, self).__init__(htmlId, cssCls=cssCls) # To get the HTML Id

  def html(self, localPath):
    """ """
    return '<button type="button" class="btn btn-%s btn-sm"><span class="glyphicon glyphicon-%s"></span></button>' % (self.btype, self.alias)

class ButtonOk(ButtonRemove):
  """
  """
  alias = 'ok'
  btype = 'success'

class A(HtmlItem):
  """ Wrapper for a Anchor HTML tag """
  val, link = None, None
  alias = 'anchor'

  def __init__(self, htmlId, value, link, cssCls=None):
    """ Set the div value """
    super(A, self).__init__(htmlId) # To get the HTML Id
    self.val = value
    self.link = link
    self.cssCls = cssCls

  def html(self, localPath):
    """ Return the HMTL object of for div """


    if self.cssCls is not None:
      return '<a href="%s" class="%s">%s</a>' % (self.link, self.val, self.cssCls)

    return '<a href="%s">%s</a>' % (self.link, self.val)



class Text(HtmlItem):
  """
  """
  cssCls = None
  val = None
  alias = 'text'

  def __init__(self, htmlId, value, cssCls=None):
    """ """
    super(Text, self).__init__(htmlId) # To get the HTML Id
    self.val = value
    if cssCls is not None:
      self.cssCls = cssCls

  def html(self, localPath):
    """ """
    if self.cssCls is not None:
      return '<font id="%s" class="%s">%s</font>' % (self.htmlId, self.cssCls, self.val)

    return '<font id="%s">%s</font>' % (self.htmlId, self.val)

class Code(Text):
  """ """
  cssCls = ''
  alias = 'code'

  def html(self, localPath):
    """ """
    if self.cssCls is not None:
      return '<pre><code id="%s" class="%s">%s</code></pre>' % (self.htmlId, self.cssCls, self.val)

    return '<pre><code id="%s">%s</code></pre>' % (self.htmlId, self.val)

class Paragraph(HtmlItem):
  """
  """
  cssCls = None
  val = None
  htmlObjs = None
  alias = 'paragraph'

  def __init__(self, htmlId, value, htmlObjs=None, cssCls=None):
    """ """
    super(Paragraph, self).__init__(htmlId) # To get the HTML Id
    self.val = value
    self.cssCls = cssCls
    self.htmlObjs = htmlObjs

  def html(self, localPath):
    """ Return the HTML string for a paragraph including or not some other html object """
    # For this object we can have a list of Text objects
    pVal = self.val
    if self.htmlObjs is not None:
      for i, htmlObj in enumerate(self.htmlObjs):
        pVal = pVal.replace("{%s}" % i, htmlObj.html(localPath))
    if self.cssCls is not None:
      return '<p id="%s" class="%s">%s</p>' % (self.htmlId, self.cssCls, pVal)

    return '<p id="%s">%s</p>' % (self.htmlId, pVal)

class Input(HtmlItem):
  """
  """
  val = None
  name = None
  alias = 'input'
  jQueryEvent = ['blur']

  def __init__(self, htmlId, name, value, cssCls=None):
    """ Instanciate the object and store the name and the value of the input text """
    super(Input, self).__init__(htmlId, cssCls) # To get the HTML Id
    self.name = name
    self.val = value

  def autocomplete(self, values):
    """
    """
    jsDef= '''
            %s.autocomplete({
              source: %s
            });
           ''' % (self.jsRef(), values)
    if self.jsEvent is None:
      self.jsEvent = [('autocomplete', jsDef)]
    else:
      self.jsEvent.append(('autocomplete', jsDef))

  def html(self, localPath):
    """ """
    item = ['<div class="form-group">']
    item.append('%s<label for="pwd">%s:</label>' % (INDENT, self.name))
    item.append('%s<input type="text" class="form-control" id="%s" value="%s">' % (INDENT, self.htmlId, self.val))
    item.append('</div>')
    return "\n".join(item)

class Comment(HtmlItem):
  """
  """
  val = None
  name = None
  alias = 'comment'
  jQueryEvent = ['blur']

  def __init__(self, htmlId, name, value, cssCls=None):
    """ Instanciate the object and store the name and the value of the input text """
    super(Comment, self).__init__(htmlId, cssCls) # To get the HTML Id
    self.name = name
    self.val = value

  def html(self, localPath):
    """ """
    item = ['<div class="form-group">']
    item.append('%s<label for="pwd">%s:</label>' % (INDENT, self.name))
    item.append('%s<textarea class="form-control" rows="5" id="%s">%s</textarea>' % (INDENT, self.htmlId, self.val))
    item.append('</div>')
    return "\n".join(item)

class TextArea(HtmlItem):
  """

  """
  alias = 'textarea'
  jsclick = False

  def html(self, localPath):
    """ Return the item with a text area and a button """
    if not self.jsclick:
      print('The jsRef method will return the value of the textarea')
      raise Exception('The click method had to be defined for TextArea')

    item = ['<div class="input-group">']
    item.append('%s<textarea class="form-control custom-control" rows="3" style="resize:none" id="%s"></textarea>' % (INDENT, self.htmlId))
    item.append('%s<span class="input-group-btn"><button class="btn btn-primary" id="%s_button"><span>Send</span></button></span>)' % (INDENT, self.htmlId))
    item.append('</div>')
    return "\n".join(item)

  def jsVal(self):
    """ Return the Javascript Value """
    return '$("#%s").val()' % self.htmlId

  def text(self, val):
    """ Update the textarea value """
    return '$("#%s").html(%s)' % (self.htmlId, val)

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    return '$("#%s_button")' % self.htmlId

  def click(self, jsAction):
    """
    """
    if self.jsEvent is None:
      self.jsEvent = [('click', jsAction)]
    else:
      self.jsEvent.append(('click', jsAction))
    self.jsclick = True


class Title(HtmlItem):
  """ Wrapper for the HTML header tags

  Tooltips functionality will require jquery-ui.js
  """
  cssCls = None
  val = None
  alias = 'title'

  def __init__(self, htmlId, dim, value, tooltips=False, cssCls=None):
    """ Instanciate the object, define the level and add the class """
    super(Title, self).__init__(htmlId) # To get the HTML Id
    self.val = value
    self.cssCls = cssCls
    self.dim = dim
    self.tooltips = tooltips

  def html(self, localPath):
    """ Return a header HTML Tag """
    if self.cssCls is not None:
      return '<H%s id="%s" class="%s">%s</H%s>' % (self.dim, self.htmlId, self.cssCls, self.val, self.dim)

    return '<H%s id="%s">%s</H%s>' % (self.dim, self.htmlId, self.val, self.dim)

  def jsOnLoad(self):
    if self.tooltips:
      return "$( document ).tooltip();"

class Modal(HtmlItem):
  """ Wrapper to a simple model view """
  val = None
  name = None
  alias = 'modal'
  modal_header = '' # The title for the modal popup

  def __init__(self, htmlId, name, aresObj, cssCls=None):
    """ Instanciate the object and store the name and the value of the input text """
    super(Modal, self).__init__(htmlId, cssCls) # To get the HTML Id
    self.name = name
    self.aresObj = aresObj

  def html(self, localPath):
    """
    """

    item = ['<br /><a data-toggle="modal" data-target="#%s" style="cursor: pointer">%s</a>' % (self.htmlId, self.name )]
    item.append('<div class="modal fade" id="%s" role="dialog">' % self.htmlId)
    item.append('<div class="modal-dialog modal-sm">')
    item.append('%s<div class="modal-content">' % INDENT)
    item.append('%s%s<div class="modal-header">' % (INDENT, INDENT))
    item.append('%s%s%s<button type="button" class="close" data-dismiss="modal">&times;</button>' % (INDENT, INDENT, INDENT))
    item.append('%s%s%s<h4 class="modal-title">%s</h4' % (INDENT, INDENT, INDENT, self.modal_header))
    item.append('%s%s</div>' % (INDENT, INDENT))
    item.append('%s%s<div class="modal-body">' % (INDENT, INDENT))
    item.append(self.aresObj.html(localPath))
    item.append('%s%s</div>' % (INDENT, INDENT))
    item.append('%s<div>' % INDENT)
    item.append('<div><div>')
    return "\n".join(item)

class DatePicker(HtmlItem):
  """ Wrapper to a Jquery Date picker object

  This module will require jquery-ui.js to run correctly
  """
  cssCls = None
  val = None
  alias = 'date'

  def jsOnLoad(self):
    return "%s.datepicker();" % self.jsRef

class DropZone(HtmlItem):
  """

  """
  cssCls = None
  val = None
  alias = 'dropZone'
  jsEvent = [('dragover', '''
                          event.originalEvent.stopPropagation();
							            event.originalEvent.preventDefault();
                          event.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
                          '''),
             ('drop', '''
                          event.originalEvent.stopPropagation();
						              event.originalEvent.preventDefault();
                          var files = event.originalEvent.dataTransfer.files; // FileList object.

                          //files is a FileList of File objects. List some properties.
                          var output = [];
                          for (var i = 0, f; f = files[i]; i++) {
                             output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                                        f.size, ' bytes, last modified: ',
                                        f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                                        '</li>');
                          }
                          $('#list').html('<ul>' + output.join('') + '</ul>');

                      '''),
             ]

  def html(self, localPath):
    """ Return the Drop Zone component """
    item = ['<div style="border: 1px dotted black;text-align:center;padding:20px;background-color:#479E47" id="%s">Drop files here</div><output id="list"></output>' % self.htmlId]
    return "\n".join(item)

class DropFile(HtmlItem):
  """

  """
  cssCls = None
  val = None
  alias = 'dropFile'
  reportName = ''
  jsEvent = [('dragover', '''
                          event.originalEvent.stopPropagation();
							            event.originalEvent.preventDefault();
                          event.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
                          '''),
             ]

  def drop(self):
    """  """
    ajaxObject = AresJs.XsCallFile(self.reportName)
    ajaxObject.url = 'script_upload'
    ajaxObject.async = 'false'
    ajaxObject.success('alert(data) ;')
    return ajaxObject.ajax('form_data')

  def html(self, localPath):
    """ Return the Drop Zone component """
    self.jsEvent.append(('drop', '''
                          event.originalEvent.stopPropagation();
						              event.originalEvent.preventDefault();
                          var file = event.originalEvent.dataTransfer.files[0]; // FileList object.

                          //files is a FileList of File objects. List some properties.
                          var form_data = new FormData();
                          form_data.append('files', file);
                          %s

                      ''' % self.drop()))

    item = ['<div style="border: 1px dotted black;text-align:center;padding:20px;background-color:#479E47" id="%s">Drop files here</div><output id="list"></output>' % self.htmlId]
    return "\n".join(item)