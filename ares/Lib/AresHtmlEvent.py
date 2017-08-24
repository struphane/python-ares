""" Python Module to define all the HTML component dedicated to handle events

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs
from datetime import datetime

class Button(AresHtml.Html):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = button
  """
  alias, cssCls = 'button', 'btn btn-success'
  reference = 'https://www.w3schools.com/tags/tag_button.asp'

  def __str__(self):
    """ Return the String representation of HTML button """
    return '<button %s type="button" style="margin-bottom:10px;">%s</button>' % (self.strAttr(), self.vals)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.button("MyButton")

  def post(self, evenType, url, data, jsDef='', preAjaxJs='', redirectUrl=''):
    """
      Post method to get data directly by interacting with the page
      https://api.jquery.com/jquery.post/
    """
    # Part dedicated to run before the Ajax call
    preAjax = AresItem.Item("var %s = %s.html();" % (self.htmlId, self.jqId))
    preAjax.add(0, "%s.html('<i class=\"fa fa-spinner fa-spin\"></i> Processing'); " % self.jqId)
    preAjax.add(0, preAjaxJs)

    # Items to add during the ajax call
    itemAjax = AresItem.Item(jsDef)
    itemAjax.add(0, "%s.html(%s) ;" % (self.jqId, self.htmlId))
    super(Button, self).post(evenType, url, data, str(itemAjax), str(preAjax), redirectUrl)


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

  def __str__(self):
    """ Return the String representation of a HTML Style Twitter button """
    return '<button type="button" %s><span class="fa fa-%s">&nbsp;%s</span></button>' % (self.strAttr(), self.glyphicon, self.vals)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.remove()


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

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.download()


class ButtonDownloadAll(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = downloadAll
  """
  glyphicon, cssCls = 'cloud-download', 'btn btn-success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'downloadAll'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.downloadAll()


class ButtonOk(ButtonRemove):
  """
  Python wrapper to the HTML Button component

  Input value should be a String

  Default class parameters
    - CSS Default Class = btn btn-success
    - glyphicon = ok
  """
  glyphicon, cssCls = 'check-square-o', 'success'
  reference =  'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'
  alias = 'ok'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.ok("OK Button")


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

  def addLink(self, link, dots='..'):
    """ Add the link to another page to this object """
    if self.directory is None:
      splitUrl  = link.split("?")
      if len(splitUrl) > 1:
        link = "%s/child:%s/%s?%s" % (dots, self.reportName, self.childPages[splitUrl[0]].replace(".py", ""), splitUrl[1])
      else:
        link = "%s/child:%s/%s" % (dots, self.reportName, self.childPages[splitUrl[0]].replace(".py", ""))
      self.link = link
    else:
      # There is a child and we need to produce the sub Report attached to it
      # The below part allow also to test locally the get and post method that we put in the URL
      # Basically the Wrapper will create all tehe secondary pages using all the different parameters
      splitUrl  = link.split("?")
      childReport = self.childPages[splitUrl[0]].replace(".py", "")
      link = "%s.html" % childReport
    self.link = link

  def __str__(self):
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
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, "%s window.location = '%s' ;" % (jsDef, self.link), jsDef)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.anchor("MyAnchor")


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
    self.jsEvent['autocomplete'] = AresJs.JQueryEvents(self.htmlId, self.jqId, 'autocomplete', 'source: %s' % values)

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.attr['value'] = dflt

  def __str__(self):
    """ Return the String representation of a HTML Input object """
    item = AresItem.Item('<div class="form-group">', self.incIndent)
    item.add(1, '<label for="%s">%s:</label>' % (self.vals.replace(" ", "").lower(), self.vals))
    item.add(2, '<input type="text" style="width:100%%" %s>' %  self.strAttr())
    item.add(0, '</div>')
    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.input("Input text...")


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

  def __str__(self):
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

  def __str__(self):
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

  @property
  def val(self):
    """ Return the Javascript Value - return the val of the textarea object """
    return '$("#%s").val()' % self.htmlId

  def jsText(self, val):
    """ Update the textarea value - set the value of the textarea object """
    return '$("#%s").html(%s)' % (self.htmlId, val)

  @property
  def jqId(self):
    """ Function to return the Jquery reference to the Html object """
    return '$("#%s_button")' % self.htmlId

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.textArea("Enter text...")


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

  def __str__(self):
    """ Return the HTML String of a Drop Down list """
    item = AresItem.Item('<div %s>' % self.strAttr())
    item.add(1, '<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">%s<span class="caret"></span></button>' % self.title)
    item.add(1, '<ul class="dropdown-menu">')
    for val in self.vals:
      item.add(2, '<li><a href="#%s">%s</a></li>' % (val[0], val[1]))
    item.add(1, '</ul>')
    item.add(0, '</div>')
    return str(item)

  @property
  def jqId(self):
    """ Return the javascript reference to the dropdown li item """
    return '$("#%s .dropdown-menu li")' % self.htmlId

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.dropdown([["Super", ("A", "a"), ("B", "b")]])


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
  alias, cssCls = 'select', 'selectpicker'

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

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.select([('Node', ['GBC', 'BNPPAR'])])


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

  def __str__(self):
    """ Return the HMTL object of for div """
    return '<div %s>%s</div>' % (self.strAttr(), self.vals)

  def onloadFnc(self):
    """ Use the Jquery UI property to change the DIV in slider object """
    return AresItem.Item.indents(2, '%s.slider();' % self.jqId)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.slider(100)


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
  cssCls = 'datepicker'
  dflt = ''

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.dflt = dflt

  def __str__(self):
    """ Return the String representation of a Date picker object """
    if '-' in self.dflt:
      return '<p><strong>%s: </strong><input type="text" %s value="%s"></p>' % (self.vals, self.strAttr(), self.dflt)
    return '<p><strong>%s: </strong><input type="text" style="width:100%%" %s></p>' % (self.vals, self.strAttr())

  def onLoadFnc(self):
    """ Start the Date picker transformation when the document is loaded """
    return AresItem.Item.indents(2, "$( function() {%s.datepicker({dateFormat: 'yy-mm-dd'} ); } );" % self.jqId)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.date()


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

  def __str__(self):
    """ Return the Drop Zone component """
    return '<div style="border: 1px dotted black;text-align:center;padding:20px;background-color:#479E47" %s>%s</div>' % (self.strAttr(), self.vals)

  def onLoadFnc(self):
    return """
            $(document).on("dragover drop", function(e) {
              e.preventDefault();
            }
           """

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.dropzone("MyFiles")


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

  def __str__(self):
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

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.dropfile("MyFile")


class UploadFile(AresHtml.Html):
  """

  """
  alias = 'upload'
  clss = 'custom-file-input'

  def __str__(self):
    """ Display the file upload object """
    self.headerBox = 'Select a file '
    items = AresItem.Item('<div class="panel panel-success">')
    items.add(1, '<div class="panel-heading">')
    items.add(2, '<strong><i class="fa fa-file" aria-hidden="true"></i>&nbsp;%s</strong>' % self.headerBox)
    items.add(1, '</div>')
    items.add(1, '<div class="panel-body">')
    items.add(2, '<div class="col-lg-7" style="padding:5px">')
    items.add(3, '<label class="btn btn-default btn-file" style="width:100%%; height:100%%" id="value_%s">' % self.htmlId)
    items.add(4, 'Browse a file<input type="file" style="display: none;"  %s>' % self.strAttr())
    items.add(3, '</label>')
    items.add(3, '<button type="button" id="button_%s" class="btn btn-success" style="height:35px"><span class="fa fa-check-square-o">&nbsp;Upload</span></button>' % self.htmlId)
    items.add(2, '</div>')
    items.add(1, '</div>')
    items.add(0, '</div>')
    return str(items)

  def js(self, evenType, jsDef):
    """ Add a Javascript Event to an HTML object """
    if evenType == 'change':
      # .replace(/\\/g, "/").replace(/.*\//, "")
      jsDef = 'var input = %s; $("#value_%s").text(%s).append(input); %s' % (self.jqId, self.htmlId,  self.val, jsDef)
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, jsDef)

  def jsEvents(self, jsEventFnc=None):
    if not self.jsEvent:
      self.js('change', '')
    return super(UploadFile, self).jsEvents(jsEventFnc)

  def click(self, reportName, jsFnc='', data=None, folders=None):
    """ Generic upload method to send to file to a dedicated server location """
    data = {} if data is None else data
    self.post('click', '../upload/%s' % reportName, data, jsFnc, "/".join(folders))
    return self

  def post(self, evenType, url, data, jsDef, dstFolder, preAjaxJs=''):
    """
      Post method to get data directly by interacting with the page
      https://api.jquery.com/jquery.post/

    """
    jsRef = self.jqId
    if evenType == 'click':
      #jsDef = '$("#value_%s").val(%s); %s' % (self.htmlId, self.jsVal(), jsDef)
      jsRef = "$('#button_%s')" % self.htmlId
    jsDef = '''
        var file = $('#%s').prop('files')[0]; // FileList object.
        var form_data = new FormData();
        form_data.append('file_0', file);
        form_data.append('DESTINATION', '%s');
        %s
        $.ajax({url: "%s", method: "POST", data: form_data, contentType: false, cache: false, processData: false, async: false}).done(function(data) {%s location.reload(); } );
                ''' % (self.htmlId, dstFolder, preAjaxJs, url, jsDef)
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, jsRef, evenType, jsDef, data=data, url=url)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.upload("MyFile")


class GeneratePdf(ButtonRemove):
  alias = "generatePdf"
  glyphicon, cssCls = "book", "btn btn-default"
  source = r"http://pdfmake.org/#/gettingstarted"

  def __init__(self, aresObj, fileName=None, cssCls=None): # Hack: I need the whole aresObj as param since I need to retrieve everything that has been created so far
    super(GeneratePdf, self).__init__(aresObj.getNext(), "", cssCls)

    if fileName is None:
      fileName = "%s_%s" % (aresObj.reportName if hasattr(aresObj, "reportName") else "ares_export", datetime.now())

    self.jsEvent["var"] = "var docDefinition = { content: 'This is an sample PDF printed with pdfMake' };"
    self.jsEvent["click"] = AresJs.JQueryEvents(self.htmlId, '$("#%s")' % self.htmlId, "click", "pdfMake.createPdf(docDefinition).download('%s.pdf');" % fileName)



if __name__ == '__main__':
  obj = DropZone(0, 'Drop files here')
  print('\n'.join(obj.jsEvents()))
  print('\n'.join(obj.onLoad()))
  print(obj)

  obj = DatePicker(0, 'Drop files here')
  print('\n'.join(obj.jsEvents()))
  print('\n'.join(obj.onLoad()))
  print(obj)
