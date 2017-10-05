"""
Definition of all the different HTML button wrappers.
From this module lot of different sort of HTML buttons can be displayed like:
  - ButtonDownload, the button dedicated to download files
  - ButtonRefresh, the button dedicated to query another script in the framework and then to refresh data
  - ButtonOk, to validate something and return a notification
  - GeneratePdf, to generate a Pdf report

Also it is possible to use the generic and basic button object - Button - to then change it to a specific one in your report.
Some based functions are available in order to change more or less everything in the python
"""


import os
import json

from ares.Lib import AresHtml
from ares.Lib.html import AresHtmlContainer

class Meter(AresHtml.Html):
  """
  """
  alias, cssCls = 'meter', ['ares-meter']
  reference = ''
  reqCss = []
  reqJs = ['meter']
  references = []

  def __init__(self, aresObj, headerBox, value, cssCls=None, cssAttr=None):
    """Initialise a new meter object.

    ARGUMENTS
    ---------
    value: Floating point number in range [0..1] representing the meter state percentage
    """
    if value < 0 or value > 1:
      raise ValueError('Value must be in range 0..1')

    super(Meter, self).__init__(aresObj, [], cssCls, cssAttr)
    self.headerBox = headerBox
    self.value = value

  def __str__(self):
    """ Return the String representation of HTML button """
    strItem = '<div %s></div><script>var %s = meter("%s", %f);</script>' % (self.strAttr(), self.htmlId, self.htmlId, self.value)
    if self.headerBox is not None:
      return str(AresHtmlContainer.AresBox(self.htmlId, strItem, self.headerBox))
    return strItem

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.meter(.75)
