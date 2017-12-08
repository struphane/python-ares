""" Python Module to define all the HTML Bespoke Modals (popup)

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

from ares.Lib.html import AresHtmlSelect
from ares.Lib.html import AresHtmlEvent


class Modal(AresHtml.Html):
  """
  Python Wrapper to a simple modal view

  Default class parameters
    - CSS Default Class = table

  """
  cssCls, alias = ['modal fade'], 'modal'
  modal_header = '' # The title for the modal popup
  reference = 'https://v4-alpha.getbootstrap.com/components/modal/'
  maxHeight = 450

  def __init__(self, aresObj, name, cssCls=None, cssAttr=None, btnCls=None):
    """ Create an python HTML object """
    super(Modal, self).__init__(aresObj, None, cssCls, cssAttr)
    self.name = name
    self.vals, self.httpParams = [], {}
    if not btnCls:
      btnCls = ['btn btn-primary']
    self.btnCls = btnCls

  def addVal(self, httpKey, htmlObj):
    """ Add an HTML object to the modal """
    self.vals.append(htmlObj)
    if httpKey is not None:
      self.httpParams[httpKey] = htmlObj
    return htmlObj

  def __str__(self):
    """ Return the String representation of a HTML Modal Object """
    item = AresItem.Item('<button type="button" class="%s" data-toggle="modal" data-target="#%s" style="cursor: pointer">%s</button>' % (' '.join(self.btnCls), self.htmlId, self.name), self.incIndent)
    item.add(0, '<div %s tabindex="-1" role="dialog" aria-labelledby="%sTitle" aria-hidden="true">' % (self.strAttr(), self.htmlId))
    item.add(1, '<div class="modal-dialog">')
    item.add(2, '<div class="modal-content">')
    item.add(3, '<div class="logo_small" id="%sTitle">%s</div>' % (self.htmlId, self.modal_header))
    #item.add(4, '<button type="button" style="margin-top:10px" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>')
    #item.add(4, '<div class="modal-title" id="%sTitle">%s</div>' % (self.htmlId, self.modal_header))
    #item.add(3, '</div>')
    item.add(3, '<div class="modal-body" style="overflow-y:scroll;max-height:%spx;margin-bottom:10px">' % self.maxHeight)
    for val in self.vals:
      if hasattr(val, 'incIndent'):
          val.incIndent = 4
          item.add(0, str(val))
      else:
        item.add(4, str(val))
    item.add(3, '</div>')
    item.add(2, '</div>')
    item.add(1, '</div>')
    item.add(0, '</div>')
    return str(item)

  # -------------------------------------------------------------------------------------------------------------------
  #
  #                             Section dedicated to set the HTMO object for the modal
  # -------------------------------------------------------------------------------------------------------------------
  def input(self, label, httpKey, dflt='', cssCls=None):
    return self.addVal(httpKey, self.aresObj.input(label, cssCls=cssCls, dflt=dflt, inReport=False))

  def inputInt(self, label, httpKey, dflt='', cssCls=None):
    return self.addVal(httpKey, self.aresObj.inputInt(label, cssCls=cssCls, dflt=dflt, inReport=False))

  def date(self, label='Date', httpKey='date', dflt='', cssCls=None):
    return self.addVal(httpKey, self.aresObj.date(label, cssCls=cssCls, dflt=dflt, inReport=False))

  def internalLink(self, linkValue, script, attrs=None, cssCls=None, cssAttr=None):
    return self.addVal(None, self.aresObj.internalLink(linkValue, script, attrs=attrs, cssCls=cssCls, cssAttr=cssAttr, inReport=False))

  def radio(self, recordSet, httpKey, col=None, cssCls=None, cssAttr=None, checked=None):
    return self.addVal(httpKey, self.aresObj.radio(recordSet, col=col, cssCls=cssCls, cssAttr=cssAttr, checked=checked, inReport=False))

  def select(self, recordSet, title, httpKey, col=None, cssCls=None, cssAttr=None, selected=None):
    return self.addVal(httpKey, self.aresObj.select(recordSet, title, col=col, cssCls=cssCls, cssAttr=cssAttr, selected=selected, inReport=False))

  def selectfiles(self, fileName, title, httpKey, cssCls=None, cssAttr=None, selected=None):
    return self.addVal(httpKey, AresHtmlSelect.Select(self.aresObj, self.aresObj.fileMap.get(fileName, []), title, col=None, cssCls=cssCls, cssAttr=cssAttr, selected=selected))

  def slider(self, value, title, httpKey, cssCls=None, cssAttr=None):
    return self.addVal(httpKey, AresHtmlEvent.Slider(self.aresObj, value, title, cssCls=cssCls, cssAttr=cssAttr))

  def pwd(self, label, httpKey, dflt='', cssCls=None):
    return self.addVal(httpKey, self.aresObj.pwd(label, cssCls=cssCls, dflt=dflt, inReport=False))

  def button(self, value, httpKey, cssCls=None, cssAttr=None, awsIcon=None):
    return self.addVal(httpKey, self.aresObj.button(value, cssCls=None, cssAttr=None, awsIcon=None, inReport=False))

class FixedModal(AresHtml.Html):
  """

  """

  def __init__(self, aresObj, name, cssCls=None, cssAttr=None):
    """ Create an python HTML object """
    super(FixedModal, self).__init__(aresObj, None, cssCls, cssAttr)
    self.name = name
    self.vals = []

  def __str__(self):
    """ Return the String representation of a HTML Modal Object """
    item = AresItem.Item('<button type="button" class="btn btn-primary" %s style="cursor: pointer">%s</button>' % (self.strAttr(), self.name), self.incIndent)
    self.js('click',
            '''
              $('#popup-info').css('top', '110px');
              $('#popup-info').css('left', '110px');
              $('#popup-black-background').toggle();
              $('#popup-info').toggle();
            ''')
    return str(item)


class DialogValid(AresHtml.Html):
  """

  """
  reqCss = ['bootstrap', 'font-awesome', 'jquery']
  reqJs = ['bootstrap', 'jquery']
  references = ['https://jqueryui.com/dialog/']

  def __init__(self, aresObj, vals, title, cssCls=None, cssAttr=None):
    """ Instantiate the Dialog popup object """
    super(DialogValid, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.title = title

  def append(self, item):
    """ """

  def __str__(self):
    """ Return the HTML String representation of a Jquery Dialog popup """
    return '<div %s title=\'%s\'>%s</div>' % (self.title, self.content)

  def toJs(self, parent):
    """ Convert to a Js expression """
    return ".append('%s')" % (parent, self)


