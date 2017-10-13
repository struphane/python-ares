"""


"""


from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs


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
  cssCls, rows, dflt = ['form-control'], 5, ''
  references = ['https://www.w3schools.com/tags/tag_textarea.asp']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

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
  cssCls, rows, dflt = ['form-control', 'custom-control'], 5, ''
  references = ['https://www.w3schools.com/tags/tag_textarea.asp']
  alias = 'textArea'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.dflt = dflt

  def __str__(self):
    """ Return the item with a text area and a button """
    return str('<textarea %s rows="%s" style="resize:none;cursor:pointer;margin-bottom:30px">%s</textarea>' % (self.strAttr(), self.rows, self.dflt))

  @property
  def val(self):
    """ Return the Javascript Value - return the val of the textarea object """
    return '$("#%s").val()' % self.htmlId

  def jsText(self, val):
    """ Update the textarea value - set the value of the textarea object """
    return '$("#%s").html(%s)' % (self.htmlId, val)

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
  title, cssCls = 'Title', ['dropdown']
  alias = 'dropdown'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

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
  alias, cssCls = 'select', ['form-control']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

  def __init__(self, aresObj, vals, selected, cssCls=None, cssAttr=None):
    """ Instanciate the object and store the selected item """
    super(Select, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.selected = selected

  def __str__(self):
    """ Return the HTML string for a select """
    item = AresItem.Item('<div class="form-group">', self.incIndent)
    item.add(1, '<label for="sel1">Select list:</label>')
    item.add(1, '<select %s style="height:32px">' % self.strAttr())
    for v in self.vals:
      if v == self.selected:
        item.add(2, '<option selected>%s</option>' % v)
      else:
        item.add(3, '<option >%s</option>' % v)
    item.add(1, '</select>')
    item.add(0, '</div>')
    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.select([('Node', ['GBC', 'BNPPAR'])])


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
  references = ['https://jqueryui.com/slider/']
  alias = 'slider'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __str__(self):
    """ Return the HMTL object of for div """
    return '<div %s>%s</div>' % (self.strAttr(), self.vals)

  def onloadFnc(self):
    """ Use the Jquery UI property to change the DIV in slider object """
    return AresItem.Item.indents(2, '%s.slider();' % self.jqId)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.slider(100)


class DropZone(AresHtml.Html):
  """

  """
  alias = 'dropzone'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

  def __init__(self, aresObj, vals, cssCls=None):
    super(DropZone, self).__init__(aresObj, vals, cssCls)
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
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None):
    super(DropFile, self).__init__(aresObj, vals, cssCls, cssAttr)
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
  cssCls = ['custom-file-input']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']

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



