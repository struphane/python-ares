""" Python Module to define all the HTML Bespoke Modals (popup)

"""

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

  def __init__(self, htmlId, name, cssCls=None):
    """ Create an python HTML object """
    super(Modal, self).__init__(htmlId, None, cssCls)
    self.name = name
    self.vals = []

  def addVal(self, htmlObj):
    """ Add an HTML object to the modal """
    self.vals.append(htmlObj)

  def __repr__(self):
    """ Return the String representation of a HTML Modal Object """
    item = AresItem.Item('<a data-toggle="modal" data-target="#%s" style="cursor: pointer">%s</a>' % (self.htmlId, self.name), self.incIndent)
    item.add(0, '<div %s role="dialog">' % self.strAttr())
    item.add(1, '<div class="modal-dialog modal-sm">')
    item.add(2, '<div class="modal-content">')
    item.add(3, '<div class="modal-header">')
    item.add(4, '<button type="button" class="close" data-dismiss="modal">&times;</button>')
    item.add(4, '<h4 class="modal-title">%s</h4>' % self.modal_header)
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


if __name__ == '__main__':
  obj = Modal(0, 'Hey', [['Olivier', 'Aurelie'], [1, 2]])
  print(obj)