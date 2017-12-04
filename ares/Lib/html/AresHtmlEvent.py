""" HTML Module from some HTML object attached to bespoke events

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
  reqCss = ['bootstrap', 'jquery']
  reqJs = ['bootstrap', 'jquery']
  hasChangeEvent = False

  def __init__(self, aresObj, vals, title=None, cssCls=None, cssAttr=None):
    super(Slider, self).__init__(aresObj, vals, cssCls=cssCls, cssAttr=cssAttr)
    self.title = title

  def __str__(self):
    """ Return the HMTL object of for div """
    if not self.hasChangeEvent:
      self.change('')
    self.jsFormulas = None
    self.aresObj.jsOnLoadFnc.add('%s.slider({value: %s});' % (self.jqId, self.vals))
    if self.title is not None:
      return '<div class="form-group"><label>%s:</label><div style="text-align:center;"><div id="%s_val" style="display:inline-block;">%s</div><div %s></div></div></div>' % (self.title, self.htmlId, self.vals, self.strAttr())

    return '<div style="text-align:center;"><div id="%s_val" style="display:inline-block;">%s</div><div %s></div></div>' % (self.htmlId, self.vals, self.strAttr())

  def change(self, jsFnc):
    """ Action to update the HTML Input text box """
    self.hasChangeEvent = True
    self.aresObj.jsOnLoadFnc.add('%s.on("slidechange", function(event, ui) {  $("#%s_val").html(ui.value) ; %s });' % (self.jqId, self.htmlId, jsFnc) )

  def formulas(self, jsFormulas):
    """ """
    self.jsFormulas = jsFormulas

  def update(self, htmlObjs=None, effects=None):
    """ """
    jsEffects = effects if effects is not None else []
    objUpdate = []
    val = self.jsFormulas if self.jsFormulas is not None else self.val
    if htmlObjs is not None:
      for htmlObj in htmlObjs:
        objUpdate.append(htmlObj.jsUpdate(val))
    self.aresObj.jsOnLoadFnc.add('''
      $('#%(htmlId)s').on('slidechange', function (event, ui){
        %(objUpdt)s ; %(jsEffects)s ;
      }) ;
      ''' % {'htmlId': self.htmlId, 'data': val, 'objUpdt': '; '.join(objUpdate), 'jsEffects': ';'.join(jsEffects)})


  @property
  def val(self):
    """ Property to get the jquery value of the HTML object in a python HTML object """
    return "parseFloat($('#%s_val').html())" % self.htmlId


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
    super(UploadFile, self).js(evenType, jsDef)

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
    self.aresObj.jsOnLoadFnc.add(AresJs.JQueryEvents(self.htmlId, jsRef, evenType, jsDef, data=data, url=url))




