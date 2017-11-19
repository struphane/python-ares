""" Python Module to define all the HTML Bespoke Modals (popup)

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

class Modal(AresHtml.Html):
  """
  Python Wrapper to a simple modal view

  Default class parameters
    - CSS Default Class = table

  """
  cssCls, alias = ['modal fade'], 'modal'
  modal_header = '' # The title for the modal popup
  reference = 'https://v4-alpha.getbootstrap.com/components/modal/'

  def __init__(self, aresObj, name, cssCls=None, cssAttr=None, btnCls=None):
    """ Create an python HTML object """
    super(Modal, self).__init__(aresObj, None, cssCls, cssAttr)
    self.name = name
    self.vals = []
    if not btnCls:
      btnCls = ['btn btn-primary']
    self.btnCls = btnCls

  def addVal(self, htmlObj):
    """ Add an HTML object to the modal """
    self.vals.append(htmlObj)

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
    item.add(3, '<div class="modal-body">')
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