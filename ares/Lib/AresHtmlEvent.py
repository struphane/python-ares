""" Python Module to define all the HTML component dedicated to handle events

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

class Button(AresHtml.Html):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = button
  """
  alias, cssCls = 'button', 'btn'
  reference = 'https://www.w3schools.com/tags/tag_button.asp'

  def __repr__(self):
    """ Return the String representation of HTML button """
    return '<button %s type="button">%s</button>' % (self.strAttr(), self.vals)


class ButtonRemove(AresHtml.Html):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-danger
    - glyphicon = remove
  """
  glyphicon, cssCls = 'remove', 'btn btn-danger'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'remove'

  def __repr__(self):
    """ Return the String representation of a HTML Style Twitter button """
    return '<button type="button" %s><span class="glyphicon glyphicon-%s"></span></button>' % (self.strAttr(), self.glyphicon)


class ButtonDownload(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = download
  """
  glyphicon, cssCls = 'download', 'btn btn-success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'download'


class ButtonDownloadAll(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = downloadAll
  """
  glyphicon, cssCls = 'download-alt', 'btn btn-success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'downloadAll'


class ButtonOk(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = ok
  """
  glyphicon, cssCls = 'ok', 'success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'ok'


class A(AresHtml.Html):
  """
  Wrapper for a Anchor HTML tag

  """
  link, alias = '', 'anchor'
  reference = 'https://www.w3schools.com/tags/att_a_href.asp'

  def __init__(self, htmlId, vals, reportName, childPages, directory, cssCls=None):
    super(A, self).__init__(htmlId, vals, cssCls)
    self.childPages = childPages
    self.reportName = reportName
    self.directory = directory

  def addLink(self, link):
    """ Add the link to another page to this object """
    if self.directory is None:
      splitUrl  = link.split("?")
      if len(splitUrl) > 1:
        link = "./child:%s/%s?%s" % (self.reportName, self.childPages[splitUrl[0]].replace(".py", ""), splitUrl[1])
      else:
        link = "./child:%s/%s" % (self.reportName, self.childPages[splitUrl[0]].replace(".py", ""))
      self.link = link
    else:
      # There is a child and we need to produce the sub Report attached to it
      # The below part allow also to test locally the get and post method that we put in the URL
      # Basically the Wrapper will create all tehe secondary pages using all the different parameters
      splitUrl  = link.split("?")
      childReport = self.childPages[splitUrl[0]].replace(".py", "")
      link = "%s.html" % childReport
    self.link = link

  def __repr__(self):
    """ Return the String representation of a Anchor HTML object """
    if self.link is None:
      self.link = '#' if self.jsEvent is not None else self.link
    return '<a href="%s" %s>%s</a>' % (self.link , self.strAttr(), self.vals)

  def preload(self, evenType, jsDef='', preloading=True):
    """
    Common implementation to add javascript callback functions

    This javascript wrapper include on purpose a defined set of javascript methods in order to control the calls
    If some Ajax / DB calls are required, users will have to directly defined those items when they are writing
    the python report
    """
    if preloading:
      jsDef = "preloader(); %s" % jsDef
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jsRef(), evenType, "%s window.location = '%s' ;" % (jsDef, self.link), jsDef)


class Input(AresHtml.Html):
  """
  Python wrapper to the HTML INPUT component

  Input value should be a String

  Default class parameters
    - CSS Default Class = form-control
  """
  cssCls, alias = 'form-control', 'input'

  def autocomplete(self, values):
    """ Fill the auto completion box with a data source """
    self.jsEvent['autocomplete'] = AresJs.JQueryEvents(self.htmlId, self.jsRef(), 'autocomplete', 'source: %s' % values)

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.attr['value'] = dflt

  def __repr__(self):
    """ Return the String representation of a HTML Input object """
    item = AresItem.Item('<div class="form-group">', self.incIndent)
    item.add(1, '<label for="%s">%s:</label>' % (self.vals.replace(" ", "").lower(), self.vals))
    item.add(2, '<input type="text" %s>' % (self.strAttr()))
    item.add(0, '</div>')
    return str(item)


class Comment(AresHtml.Html):
  """
  Python wrapper to a Bespoke Comment component
  This component is built with
    - A DIV
    - A LABEL
    - A TEXTAREA

  Input value should be a String and it correspond to the label value
  The javascript references will point to the Texterea to get the object and the value

  Default class parameters
    - CSS Default Class = form-control
    - rows = 5 (the size of the Textarea)
    - dflt - '' (The default value of the Textarea)
  """
  cssCls, rows, dflt = 'form-control', 5, ''
  reference = 'https://www.w3schools.com/tags/tag_textarea.asp'

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.dflt = dflt

  def __repr__(self):
    """ Return the String representation of a HTML Comment input section """
    item = AresItem.Item('<div class="form-group">', self.incIndent)
    item.add(1, '<label for="%s">%s:</label>' % (self.vals.replace(" ", "").lower(), self.vals))
    item.add(2, '<textarea %s rows="%s" >%s</textarea>' % (self.strAttr(), self.rows, self.dflt))
    item.add(0, '</div>')
    return str(item)


class TextArea(AresHtml.Html):
  """
  Python wrapper to a Textarea Comment component
  This component is built with
    - A DIV
    - A TEXTAREA
    - A SPAN
    - A BUTTON
    - A SPAN

  Input value should be a String and it correspond to the label value
  The javascript value function will point to the Texterea
  The javascript reference will point to the button to add Jquery events

  Default class parameters
    - CSS Default Class = form-control custom-control
    - rows = 3 (the size of the Textarea)
    - dflt - '' (The default value of the Textarea)
  """
  cssCls, rows, dflt = 'form-control custom-control', 3, ''
  reference = 'https://www.w3schools.com/tags/tag_textarea.asp'
  alias = 'textArea'

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.dflt = dflt

  def __repr__(self):
    """ Return the item with a text area and a button """
    item = AresItem.Item('<div class="input-group">')
    item.add(1, '<textarea %s rows="%s" style="resize:none">%s</textarea>' % (self.strAttr(), self.rows, self.dflt))
    item.add(1, '<span class="input-group-btn">')
    item.add(2, '<button class="btn btn-primary" id="%s_button">')
    item.add(3, '<span>Send</span>')
    item.add(2, '</button>')
    item.add(1, '</span>')
    item.add(0, '</div>')
    return str(item)

  def jsVal(self):
    """ Return the Javascript Value - return the val of the textarea object """
    return '$("#%s").val()' % self.htmlId

  def jsText(self, val):
    """ Update the textarea value - set the value of the textarea object """
    return '$("#%s").html(%s)' % (self.htmlId, val)

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    return '$("#%s_button")' % self.htmlId


class DropDown(AresHtml.Html):
  """
  Wrapper for a Dropdowm HTML object

  This component is built with
    - BUTTON
    - UL
    - LI

  Input value should be a List of String or of HTML components
  The javascript reference will point to the li component

  Default class parameters
    - title = Title
    - jQueryEvent = click
    - CSS Default Class = dropdown (Bootstrap default style)
  """
  title, cssCls = 'Title', 'dropdown'
  alias = 'dropdown'

  def __repr__(self):
    """ Return the HTML String of a Drop Down list """
    item = AresItem.Item('<div %s>' % self.strAttr())
    item.add(1, '<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">%s<span class="caret"></span></button>' % self.title)
    item.add(1, '<ul class="dropdown-menu">')
    for val in self.vals:
      item.add(2, '<li><a href="#%s">%s</a></li>' % (val[0], val[1]))
    item.add(1, '</ul>')
    item.add(0, '</div>')
    return str(item)

  def jsRef(self):
    """ Return the javascript reference to the dropdown li item """
    return '$("#%s .dropdown-menu li")' % self.htmlId


class Select(AresHtml.Html):
  """
  Basic wrapper to the Select HTML Tag
    https://silviomoreto.github.io/bootstrap-select/examples/

  For example to get a change on the Select Box Item in the Javascript call back method
    - alert($(this).val()) ;

  For example
    [('Fruit', ['Apple', 'Banana'])]

  Default class parameters
  cssCls = selectpicker
  """
  # TODO: Extend the python object to handle multi select and all the cool features
  alias, cssCls = 'select', 'selectpicker'

  def __repr__(self):
    """ Return the HTML string for a select """
    item = AresItem.Item('<select %s>' % self.strAttr(), self.incIndent)
    for group, vals in self.vals:
      item.add(1, '<optgroup label="%s">' % group)
      for v in vals:
        item.add(2, '<option>%s</option>' % v)
      item.add(1, '</optgroup>')
    item.add(0, '</select>')
    return str(item)


class Slider(AresHtml.Html):
  """
  Wrapper for a Slider HTML object

  This component is built with
    - BUTTON
    - UL
    - LI

  Input value should be a float
  """
  reference = 'https://jqueryui.com/slider/'
  requirements = ['jquery-ui.js']
  alias = 'slider'

  def __repr__(self):
    """ Return the HMTL object of for div """
    return '<div %s>%s</div>' % (self.strAttr(), self.vals)

  def onloadFnc(self):
    """ Use the Jquery UI property to change the DIV in slider object """
    return AresItem.Item.indents(2, '%s.slider();' % self.jsRef())


class DatePicker(AresHtml.Html):
  """
  Wrapper to a Jquery Date picker object

  This component is built with
    - P
    - INPUT

  """
  reference = 'https://jqueryui.com/datepicker/'
  requirements = ['jquery-ui.js']
  alias = 'date'

  def __repr__(self):
    """ Return the String representation of a Date picker object """
    return '<p>Date: <input type="text" %s></p>' % self.strAttr()

  def onloadFnc(self):
    """ Start the Date picker transformation when the document is loaded """
    return AresItem.Item.indents(2, "%s.datepicker();" % self.jsRef())


class DropZone(AresHtml.Html):
  """

  """
  alias = 'dropzone'

  def __init__(self, htmlId, vals, cssCls=None):
    super(DropZone, self).__init__(htmlId, vals, cssCls)
    self.js('dragover',
            '''
              event.originalEvent.stopPropagation();
              event.originalEvent.preventDefault();
              event.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
            '''
            )
    self.js('drop',
            '''
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
          ''')

  def __repr__(self):
    """ Return the Drop Zone component """
    return '<div style="border: 1px dotted black;text-align:center;padding:20px;background-color:#479E47" %s>%s</div>' % (self.strAttr(), self.vals)

  def onLoadFnc(self):
    return """
            $(document).on("dragover drop", function(e) {
              e.preventDefault();
            }
           """


class DropFile(AresHtml.Html):
  """

  """
  alias = 'dropfile'
  reportName = ''

  def __init__(self, htmlId, vals, cssCls=None):
    super(DropFile, self).__init__( htmlId, vals, cssCls)
    self.js('dragover', '''
                          event.originalEvent.preventDefault();
                          event.originalEvent.stopPropagation();
                          event.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
                          ''')
    self.js('dragleave', '''
                          event.originalEvent.preventDefault();
                          event.originalEvent.stopPropagation();
                          event.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
                          ''')
    self.js('dragenter', '''
                          event.originalEvent.preventDefault();
                          event.originalEvent.stopPropagation();
                          event.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
                          ''')
  def drop(self):
    """  """
    ajaxObject = AresJs.XsCallFile(self.reportName)
    ajaxObject.url = 'upload'
    ajaxObject.async = 'false'
    ajaxObject.success('location.href = "/reports/page/%s";' % self.reportName)
    return ajaxObject.ajax('form_data')

  def __repr__(self):
    """
    """
    self.js('drop', '''
                      event.originalEvent.preventDefault();
                      event.originalEvent.stopPropagation();
                      var file = event.originalEvent.dataTransfer.files; // FileList object.

                      //files is a FileList of File objects. List some properties.
                      var form_data = new FormData();
                      $.each(event.originalEvent.dataTransfer.files, function(i, file) {
                        form_data.append('file_' + i, file);
                        i ++;
                      });
                      %s
                    ''' % self.drop())
    items = AresItem.Item('<div ondrop="drop(event)" style="border: 1px dotted black;text-align:center;padding:5px;background-color:#F8F8F8" %s>' % self.strAttr())
    items.add(1, "<h3>")
    items.add(2, "<b>%s</b>" % self.vals) # + Add Scripts
    items.add(1, "</h3>")
    items.add(1, "Drop scripts here to upload")
    items.add(0, "</div>")
    return str(items)



if __name__ == '__main__':
  obj = DropZone(0, 'Drop files here')
  print('\n'.join(obj.jsEvents()))
  print('\n'.join(obj.onLoad()))
  print(obj.__repr__())

  obj = DatePicker(0, 'Drop files here')
  print('\n'.join(obj.jsEvents()))
  print('\n'.join(obj.onLoad()))
  print(obj.__repr__())
