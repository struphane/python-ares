""" Python Module to define all the HTML Bespoke Modals (popup)

"""

from click import echo

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Modal(AresHtml.Html):
  """
  Python Wrapper to a simple modal view

  Default class parameters
    - CSS Default Class = table

  """
  cssCls, alias = 'modal fade', 'modal'
  modal_header = '' # The title for the modal popup
  reference = 'https://v4-alpha.getbootstrap.com/components/modal/'
  default = {'color': '#398438', 'font-family': 'anchorjs-icons', 'font-style': 'normal', 'font-varian': 'normal', 'font-weight': 'normal', 'line-height': 'inherit'}

  def __init__(self, aresObj, name, cssCls=None):
    """ Create an python HTML object """
    super(Modal, self).__init__(aresObj, None, cssCls)
    self.name = name
    self.vals = []

  def addVal(self, htmlObj):
    """ Add an HTML object to the modal """
    self.vals.append(htmlObj)

  def __str__(self):
    """ Return the String representation of a HTML Modal Object """
    item = AresItem.Item('<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#%s" style="cursor: pointer">%s</button>' % (self.htmlId, self.name), self.incIndent)
    item.add(0, '<div %s tabindex="-1" role="dialog" aria-labelledby="%sTitle" aria-hidden="true">' % (self.strAttr(), self.htmlId))
    item.add(1, '<div class="modal-dialog">')
    item.add(2, '<div class="modal-content">')
    item.add(3, '<div class="modal-header" style="padding-top: 32px">')
    item.add(4, '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>')
    self.style = dict(self.default)
    styleStr = ";".join(["%s:%s" % (key, val) for key, val in self.style.items()])
    item.add(4, '<h4 class="modal-title" id="%sTitle" style="%s">%s</h4>' % (self.htmlId, styleStr, self.modal_header))
    item.add(3, '</div>')
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

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.modal("My modal")

if __name__ == '__main__':
  obj = Modal(0, 'Hey', [['Olivier', 'Aurelie'], [1, 2]])
  echo(obj)
