""" Ares module to produce an indented object

It is much convenient to use this object with the auto indentation in order to check the result
of a report in the HTML page. The Item object will take care of the nested object and it will increment the
indentation.

Data are stored in a list of tuple and the computation of the number of indents is only done at the end to ensure
that we can adjust if the Item is in a loop. This is quite useful in the AresJs module to format the javascript functions
"""

class Item(list):
  """ Special list to nicely display the HTML objects """
  indent = '  '

  def __init__(self, val=None, incIndent=0):
    """ Append the value to the underlying list """
    self.incIndent = incIndent
    if val is not None:
      self.append((0, val))

  def add(self, countIndent, val):
    """ Append the value to the underlying list with the relevant number of indents """
    self.append((countIndent, val))

  def __repr__(self):
    """ Display the String object """
    return "\n%s" % "\n".join(["%s%s" % ("".join(int(cnt + self.incIndent) * [self.indent]), val) for cnt, val in self])

  @staticmethod
  def indents(countIndent, val):
    """ Return an indented String """
    return "%s%s" % ("".join([Item.indent for i in range(countIndent)]), val)
