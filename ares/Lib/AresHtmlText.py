"""
Definition of all the different HTML Text wrappers.

"""

import os
import locale

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Text(AresHtml.Html):
  """ Python Wrapper to the FONT HTNL Tag """
  reference = 'https://www.w3schools.com/tags/tag_font.asp'
  alias = 'text'
  htmlComp = None

  def __init__(self, aresObj, vals, cssCls=None, htmlComp=None):
    super(Text, self).__init__(aresObj, vals, cssCls)
    self.htmlComp = htmlComp

  def __str__(self):
    """ Return the String representation of a Text HTML tag """
    html = '<font %s>%s</font>' % (self.strAttr(), self.vals)
    if self.htmlComp is not None:
      html = html.format(*self.htmlComp)
    return html

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.text("My dummy text")


class Code(AresHtml.Html):
  """ Python Wrapper to the Bootsrap CODE Tag """
  reference = 'https://v4-alpha.getbootstrap.com/content/code/'
  alias = 'code'
  htmlComp = None
  reqCss = ['bootstrap']

  def __init__(self, aresObj, vals, cssCls=None, htmlComp=None):
    super(Code, self).__init__(aresObj, vals, cssCls)
    self.htmlComp = htmlComp

  def __str__(self):
    """ Return the String representation of a Code HTML tag """
    html = '<code %s>%s</code>' % (self.strAttr(), self.vals)
    if self.htmlComp is not None:
      html = html.format(*self.htmlComp)
    return html

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.code("def myFct(): pass")


class Preformat(AresHtml.Html):
  """ Python Wrapper for the HTML preformatted tag """
  reference = "https://www.w3schools.com/html/html_styles.asp"
  alias = 'preformat'

  def __str__(self):
    """  String representation of the HTML object """
    return '<pre %s>%s</pre>' % (self.strAttr(), self.vals)


class Paragraph(AresHtml.Html):
  """ Python Wrapper to the HTML P Tag """
  reference = "https://www.w3schools.com/html/html_styles.asp"
  alias = 'paragraph'
  htmlComp = None

  def __init__(self, aresObj, vals, cssCls=None, htmlComp=None):
    super(Paragraph, self).__init__(aresObj, vals, cssCls)
    self.htmlComp = htmlComp

  def __str__(self):
    """ Return the String representation of a Code HTML tag """
    item = AresItem.Item('<div class="container">')
    if self.htmlComp is not None:
      self.vals = self.vals.format(*self.htmlComp)
    for val in self.vals.split("\n"):
      item.add(1, "<p class='text-justify'>%s</p>" % val.strip())
    item.add(0, '</div>')
    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    aresObj.text("My text")
    return aresObj.paragraph("My Paragraph")


class BlockQuote(AresHtml.Html):
  """ Python Wrapper to the HTML Block qutoe Bootstrap object """
  alias, cssCls = 'blockquote', 'blockquote'
  reference = 'https://v4-alpha.getbootstrap.com/content/typography/'
  reqCss = ['bootstrap']

  def __str__(self):
    """  String representation of the HTML object """
    item = AresItem.Item('<blockquote %s">' % self.strAttr())
    item.add(1, "<p>%s</p>" % self.vals[0])
    item.add(1, "<small>by <cite>%s</cite></small>" % self.vals[1])
    item.add(0 , "</blockquote>")
    return str(item)


class Title(AresHtml.Html):
  """ Python Wrapper to the HTML H1 Tag """
  dim, alias = 1, 'title'
  default = {'color': '#398438', 'cursor': 'pointer', 'font-style': 'normal', 'font-variant': 'normal', 'font-weight': 'normal', 'line-height': 'inherit'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  def addStyle(self, name, value):
    """ Add the style to the Title object """
    if self.style is None:
      self.style = dict(self.default)
    self.style[name] = value

  def __str__(self):
    """ Return a header HTML Tag """
    if not hasattr(self, 'style'):
      self.style = dict(self.default)
    styleStr = ";".join(["%s:%s" % (key, val) for key, val in self.style.items()])
    items = AresItem.Item('<H%s class="page-header" %s style="%s">' % (self.dim, self.strAttr(), styleStr))
    items.add(1, '<a class="anchorjs-link " style="%s">%s</a>' % (styleStr, self.vals))
    items.add(0, '</H%s>' % self.dim)
    return str(items)

  def onLoadFnc(self):
    """ Activate the Jquery Tooltips """
    return "$( function() { $( document ).tooltip() ; }) ;"

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title("Level 1 Title")

  @classmethod
  def aresDesigner(cls, id):
    """ Return a header HTML Tag for the Designer """
    obj = cls(id, 'Put your text her')
    return str(obj)


class Title2(Title):
  """ Python Wrapper to the HTML H2 Tag """
  dim, alias = 2, 'title2'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title2("Level 2 Title")


class Title3(Title):
  """ Python Wrapper to the HTML H3 Tag """
  dim, alias = 3, 'title3'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title3("Level 3 Title")


class Title4(Title):
  """ Python Wrapper to the HTML H4 Tag """
  dim, alias = 4, 'title4'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title4("Level 4 Title")


class Newline(AresHtml.Html):
  """ Python Wrapper to the HTML BR tag """
  reference = 'https://www.w3schools.com/tags/tag_br.asp'
  alias = 'newline'

  def __str__(self):
    """ Return the String representation of a new line tag """
    return '<br />'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.newline()


class Line(AresHtml.Html):
  """ Python Wrapper to the HTML HR tag """
  reference = 'https://www.w3schools.com/tags/tag_hr.asp'
  alias = 'line'

  def __str__(self):
    """ Return the String representation of a line tag """
    return '<hr %s/><hr %s/>' % (self.strAttr(), self.strAttr())

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.line()


class Icon(AresHtml.Html):
  """ Wrapper for the HTML awesome icons """
  reference = 'http://fontawesome.io/icons/'
  alias = 'icon'
  reqCss = ['font-awesome']

  def __str__(self):
    """ Return the String representation of a line tag """
    return '<i class="fa fa-%s" style="cursor:pointer" aria-hidden="true" %s></i>' % (self.vals, self.strAttr())

  def deleteLink(self, reportName, fileName, folders):
    """ Delete the file or the folder in the dedicated folder """
    if fileName is None:
      self.post('click', "../delete_folder/%s" % reportName, {'SOURCE_PATH': "/".join(folders)}, 'location.reload();')
    else:
      self.post('click', "../delete_file/%s" % reportName, {'SOURCE_PATH': "/".join(folders), 'FILE_NAME': fileName},
                'location.reload();')
    return self


class Numeric(AresHtml.Html):
  """ Reprsents a figure in a nice display """
  alias = 'number'
  reference = ''

  def __str__(self):
    """ Return the String representation of a line tag """
    locale.setlocale(locale.LC_ALL, '')
    html = "<font %s>{:,d}</font>" % self.strAttr()
    return html.format(int(float(self.vals)))


class Tick(AresHtml.Html):
  """ Wrapper for a numerical component with a up and down arrow """
  alias = 'tick'
  reqCss = ['font-awesome']

  def __str__(self):
    """ Return the String representation of a line tag """
    if self.vals:
      return  "<i class='fa fa-check' aria-hidden='true' style='color:green' %s></i>" % self.strAttr()

    return "<i class='fa fa-times' aria-hidden='true' %s style='color:red'></i>" % self.strAttr()


class UpDown(AresHtml.Html):
  """ Up and down Text component """
  alias = 'updown'
  default = {'color': 'green', 'cursor': 'pointer', 'font-style': 'normal', 'font-variant': 'normal',
             'font-weight': 'normal', 'line-height': 'inherit', 'font-size': '15px'}

  def __init__(self, aresObj, vals, delta, cssCls=None, htmlComp=None):
    super(UpDown, self).__init__(aresObj, vals, cssCls)
    self.delta = delta

  def addStyle(self, name, value):
    """ Add the style to the Title object """
    if self.style is None:
      self.style = dict(self.default)
    self.style[name] = value

  def __str__(self):
    """ Return the String representation of a line tag """
    if not hasattr(self, 'style'):
      self.style = dict(self.default)
    styleStr = ";".join(["%s:%s" % (key, val) for key, val in self.style.items()])
    if self.delta > 0:
      return "<i class='fa fa-arrow-up' aria-hidden='true' %s style='%s'>%s</i>" % (self.strAttr(), styleStr, Numeric(None, self.vals))

    return "<i class='fa fa-arrow-down' aria-hidden='true' %s style='%s'>%s</i>" % (self.strAttr(), styleStr, Numeric(None, self.vals))


# --------------------------------------------------------------------
# Object dedicated to be used
#      - To show an example of an HTML object
#      - In the designer to create the reports on the web interface
# --------------------------------------------------------------------
class TextInput(AresHtml.Html):
  """ special HTML object in charge of changing properties when double clicked """
  alias = 'aresInput'
  reqJs = ['jquery']
  reqCss = ['bootstrap', 'font-awesome']

  def __str__(self):
    """ Return the html string representation """
    items = AresItem.Item('<div ondblclick="$(\'#in_%s\').show() ; $(this).hide() ;" %s>%s</div>' % (self.htmlId, self.strAttr(), self.vals))
    items.add(0, '<input type="text" id="in_%s" value="%s" style="display:none;" onblur="$(\'#%s\').html($(this).val()); $(\'#%s\').show() ; $(this).hide()">' % (self.htmlId, self.vals, self.htmlId, self.htmlId))
    return str(items)


class DataSource(AresHtml.Html):
  """ special HTML object in charge of changing properties when double clicked """
  alias = 'aresDataSource'
  cssCls = 'ui-widget-header'

  def __str__(self):
    """ Return the html string representation """
    items = AresItem.Item(' <div %s><p>%s</p></div>' % (self.strAttr(), self.vals))
    return str(items)

  def onLoadFnc(self):
    """ Set the area droppable """
    return '''$( function() {
                  var droppedItem = 0 ; // This variable will be used in order to set the ID in the python
                  %s.droppable({
                      drop: function( event, ui ) {
                        event.preventDefault();
                        if ($('#%s p').text() == '%s') {$('#%s p').text('') ;}
                        var dragId = $(ui.draggable).attr('id') ;
                        var sourceValue = $(ui.draggable).text() ;
                        // $( this ).find( "p" ).html( "Dropped!" );
                        $( this ).append(dragId);
                        $('#' + dragId).text(sourceValue);
                        droppedItem++ ;
                      }
                    });
              } );
           ''' % (self.jqId, self.htmlId, self.vals, self.htmlId)


class DragItems(AresHtml.Html):
  """ special HTML object in charge of changing properties when double clicked """
  alias = 'aresDragItems'
  cssCls = 'ui-widget-content'

  def __str__(self):
    """ Return the html string representation """
    items = AresItem.Item(' <div style="cursor:pointer;width:200px" %s>' % self.strAttr())
    for val in self.vals:
      items.add(1, "  <p id='%s_%s' align='center' style='width:100%%;padding:3px'>%s</p>" % (self.htmlId, val, val) )
    items.add(9, "</div>")
    return str(items)

  def onLoadFnc(self):
    """ Set the items draggable """
    return "$( function() { $('#%s p').draggable(); } );" % self.htmlId


class Wiki(AresHtml.Html):
  """
  This object is very special and this is dedicated to manage comments
  People using this object will be able to create simpe json text file with comments for each line

  The idea of this report is to expose some information and then to alloww users to be able to update it
  The extra information will be done on dedicated files and later they can be included to the scripts
  """
  alias = 'wiki'

  def __init__(self, aresObj, dataSourceName, vals, cssCls=None):
    """ Init override in order to store the Ares Object (only the parameters"""
    super(Wiki, self).__init__(aresObj, vals, cssCls)
    self.http = aresObj.http
    self.dataSourceName = dataSourceName

  def __str__(self):
    """ Return the html string representation """
    items = AresItem.Item('<div class="page" style="margin-left:25%;margin-right:25%">')
    commentFiles = {}
    configPath = os.path.join(self.http['DIRECTORY'], 'config', self.dataSourceName)
    if not os.path.exists(configPath):
      os.makedirs(configPath)
    for pyFile in os.listdir(configPath):
      configFile = open(os.path.join(configPath, pyFile))
      content = configFile.read()
      if content != '':
        commentFiles[pyFile.replace(".cfg", "")] = content
      configFile.close()
    for i, val in enumerate(self.vals):
      objectId = "%s_%s" % (self.htmlId, i)
      items.add(1, '<div style="white-space: pre;" ondblclick="$(\'#in_%s\').show() ; $(\'#in_cmmt_%s\').focus()" id="%s">%s</div>' % (objectId, objectId, objectId, val))
      inCmmtId = 'in_cmmt_%s' % objectId
      if inCmmtId in commentFiles:
        items.add(1, '<div id="in_%s">' % objectId)
        items.add(2, '<textarea class="bubble_cmmt" id="%s" onblur="leaveBox($(\'#in_%s\'), $(this)) ;">%s</textarea>' % (inCmmtId, objectId, commentFiles[inCmmtId]))
      else:
        items.add(1, '<div id="in_%s" style="display:none;">' % objectId)
        items.add(2, '<textarea class="bubble_cmmt" id="%s" onblur="leaveBox($(\'#in_%s\'), $(this)) ;"></textarea>' % (inCmmtId, objectId))
      items.add(2, '<button type="button" class="btn btn-success" style="margin-bottom:10px;margin-left:5px" onclick="save_cmmt($(this), $(\'#in_cmmt_%s\')) ;">Save</button>' % objectId)
      items.add(2, '<button type="button" id="in_cmmt_%s_cl" class="btn btn-danger" style="margin-bottom:10px;" onclick="cancel_cmmt($(\'#in_%s\'), $(\'#in_cmmt_%s\')) ;">Cancel</button>' % (objectId, objectId, objectId))
      items.add(1, '</div>')
    items.add(0, '</div>')
    return str(items)

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return None

  def onLoadFnc(self):
    """

    """
    return """
            function leaveBox(box, cmmt) {
              if (cmmt.val() == '') { box.hide() ; }
            } ;
            
            function save_cmmt(button, cmmt) {
              $.post("/reports/json/%s", {val: cmmt.val(), key: cmmt.attr('id'), source: '%s'}, function(data) {
                button.hide();
                $('#'+ cmmt.attr('id')).attr('readonly','readonly');
                $('#'+ cmmt.attr('id') +'_cl').hide();
              } );
            } ;
            
            function cancel_cmmt(box, cmmt) {
              cmmt.val('');
              box.hide() ;
            }
           """ % (self.http['REPORT_NAME'], self.dataSourceName)
