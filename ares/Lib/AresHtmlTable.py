""" Python Module to define all the HTML component dedicated to display tables

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Table(AresHtml.Html):
  """
  Python Wrapper to the HTML TABLE, TH, TR, TD tags

  Default class parameters
    - CSS Default Class = table

  """
  cssCls, alias = 'table', 'table'
  refernce = 'https://www.w3schools.com/css/css_table.asp'

  def __repr__(self):
    """ Return the String representation of a HTML table """
    item = AresItem.Item('<table %s>' % self.strAttr(), self.incIndent)
    item.add(1, '<thead>')
    item.add(2, '<tr>')
    for header in self.vals[0]:
      item.add(3, '<th>%s</th>' % header)
    item.add(2, '</tr>')
    item.add(1, '</thead>')
    for row in self.vals[1:]:
      item.add(1, '<tr>')
      for val in row:
        item.add(2, "<td>%s</td>" % val)
      item.add(1, '</tr>')
    item.add(0, '</table>')
    return str(item)



if __name__ == '__main__':
  obj = Table(0, [['Olivier', 'Aurelie'], [1, 2]])
  print(obj)