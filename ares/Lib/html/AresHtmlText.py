"""  Definition of all the different HTML Text wrappers.

@author: Olivier Nogues
"""

import os
import locale

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib.html import AresHtmlContainer

class Text(AresHtml.Html):
  """ Python Wrapper to the FONT HTNL Tag """
  alias, references = 'text', ['https://www.w3schools.com/tags/tag_font.asp']
  __css = {'font-style': 'normal', 'font-variant': 'normal', 'font-weight': 'normal', 'line-height': 'inherit'}
  htmlComp = None

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, htmlComp=None):
    super(Text, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.htmlComp = htmlComp

  def __str__(self):
    """ Return the String representation of a Text HTML tag """
    html = '<font %s>%s</font>' % (self.strAttr(), self.vals)
    if self.htmlComp is not None:
      html = html.format(*self.htmlComp)
    return html


class Code(AresHtml.Html):
  """ Python Wrapper to the Bootsrap CODE Tag """
  alias, references = 'code', ['https://v4-alpha.getbootstrap.com/content/code/']
  htmlComp = None
  reqCss = ['bootstrap']

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, htmlComp=None):
    super(Code, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.htmlComp = htmlComp

  def __str__(self):
    """ Return the String representation of a Code HTML tag """
    html = '<code %s>%s</code>' % (self.strAttr(), self.vals)
    if self.htmlComp is not None:
      html = html.format(*self.htmlComp)
    return html


class Preformat(AresHtml.Html):
  """ Python Wrapper for the HTML preformatted tag """
  references = ["https://www.w3schools.com/html/html_styles.asp"]
  alias = 'preformat'

  def __str__(self):
    """  String representation of the HTML object """
    return '<pre %s>%s</pre>' % (self.strAttr(), self.vals)


class Paragraph(AresHtml.Html):
  """ Python Wrapper to the HTML P Tag """
  references = ["https://www.w3schools.com/html/html_styles.asp"]
  alias = 'paragraph'
  htmlComp = None

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, htmlComp=None):
    super(Paragraph, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.htmlComp = htmlComp

  def __str__(self):
    """ Return the String representation of a Code HTML tag """
    item = AresItem.Item(None)
    if self.htmlComp is not None:
      self.vals = self.vals.format(*self.htmlComp)
    for val in self.vals.split("\n"):
      item.add(1, "<p class='text-justify'>%s</p>" % val.strip())
    if self.aresObj.withContainer:
      return str(AresHtmlContainer.TextContainer(self.aresObj, str(item)))

    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    aresObj.text("My text")
    return aresObj.paragraph("My Paragraph")


class BlockQuote(AresHtml.Html):
  """ Python Wrapper to the HTML Block qutoe Bootstrap object """
  alias, cssCls = 'blockquote', 'blockquote'
  references = ['https://v4-alpha.getbootstrap.com/content/typography/']
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
  __css = {'color': '#398438', 'font-weight': 'normal'}
  references = ['https://www.w3schools.com/tags/tag_hn.asp']

  def __str__(self):
    """ Return a header HTML Tag """
    items = AresItem.Item('<H%s>' % self.dim)
    items.add(1, '<a class="anchorjs-link" %s style="color:inherit">%s</a>' % (self.strAttr(), self.vals))
    items.add(0, '</H%s>' % self.dim)
    if self.aresObj.withContainer:
      return str(AresHtmlContainer.TextContainer(self.aresObj, str(items)))

    return str(items)

  def onLoadFnc(self):
    """ Activate the Jquery Tooltips """
    return "$( function() { $( document ).tooltip() ; }) ;"


class Title2(Title):
  """ Python Wrapper to the HTML H2 Tag """
  dim, alias = 2, 'title2'
  __css = {'color': '#398438', 'text-decoration': 'none'}
  references = ['https://www.w3schools.com/tags/tag_hn.asp']
  cssCls = []

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title2("Level 2 Title")


class Title3(Title):
  """ Python Wrapper to the HTML H3 Tag """
  dim, alias = 3, 'title3'
  __css = {'color': '#398438', 'text-decoration': 'none'}
  references = ['https://www.w3schools.com/tags/tag_hn.asp']
  cssCls = []

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title3("Level 3 Title")


class Title4(Title):
  """ Python Wrapper to the HTML H4 Tag """
  dim, alias = 4, 'title4'
  __css = {'color': '#398438', 'text-decoration': 'none'}
  references = ['https://www.w3schools.com/tags/tag_hn.asp']
  cssCls = []

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title4("Level 4 Title")


class Line(AresHtml.Html):
  """ Python Wrapper to the HTML HR tag """
  references = ['https://www.w3schools.com/tags/tag_hr.asp']
  alias = 'line'

  def __str__(self):
    """ Return the String representation of a line tag """
    return '<hr %s/><hr %s/>' % (self.strAttr(), self.strAttr())

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.line()


class Icon(AresHtml.Html):
  """ Wrapper for the HTML awesome icons """
  references = ['http://fontawesome.io/icons/']
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
    locale.setlocale(locale.LC_ALL, '')
    if self.vals:
      html = "<i class='fa fa-check' aria-hidden='true' %s style='color:green'></i>" % self.strAttr()
    else:
      html = "<i class='fa fa-times' aria-hidden='true' %s style='color:red'></i>" % self.strAttr()
    return html.format(int(float(self.vals)))


class UpDown(AresHtml.Html):
  """ Up and down Text component """
  alias = 'updown'
  __css = {'color': 'green', 'line-height': 'inherit'}
  reqCss = ['font-awesome']

  def __init__(self, aresObj, vals, delta, cssCls=None, cssAttr=None, htmlComp=None):
    super(UpDown, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.delta = delta

  def __str__(self):
    """ Return the String representation of a line tag """
    if self.delta > 0:
      return "<i class='fa fa-arrow-up' aria-hidden='true' %s>&nbsp;%s</i>" % (self.strAttr(), Numeric(None, self.vals))

    self.attr['css']['color'] = 'red'
    return "<i class='fa fa-arrow-down' aria-hidden='true' %s>&nbsp;%s</i>" % (self.strAttr(), Numeric(None, self.vals))


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


class TextWithBorder(AresHtml.Html):
  """ Python Wrapper to the HTML Block qutoe Bootstrap object """
  alias, cssCls = 'textborder', ''
  references = []
  colorBorder, coloTitle = 'green', 'green'
  width = None

  def __init__(self, aresObj, vals, title, cssCls=None, cssAttr=None):
    super(TextWithBorder, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.title = title
    self.attr.setdefault('css', {}).update({'margin-topm': '20px'})

  def __str__(self):
    """  String representation of the HTML object """
    if self.width is None:
      self.attr.setdefault('css', {}).update({'width': '%spx' % self.width})

    item = ['<div %s>' % self.strAttr()]
    item.append('<fieldset style="5px;border:1px solid %s;padding:5px;font-size:12px">' % self.colorBorder)
    item.append('<legend style="font-weight:bold;color:%s;width:auto;font-size:14px">%s</legend>%s</fieldset>' % (self.coloTitle, self.title, self.vals))
    item.append('</div>')
    return "".join(item)


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
