#
# class Notification(object):
#   """ """
#   def __init__(self, aresObj):
#     """ """
#     self.aresObj = aresObj
#

from ares.Lib import AresHtml
from ares.Lib import AresItem


class DangerAlert(AresHtml.Html):
  """

  """

  level = 'Danger'
  backgroundColor = '#f44336'
  closeButton = False
  cssCls = ['alert-danger']
  jsEvent = None

  def __init__(self, aresObj, title, value, countNotif, closeButton=False, backgroundColor=None, cssCls=None, cssAttr=None):
    """ Instantiate the Danger notification box """
    super(DangerAlert, self).__init__(aresObj, '', self.cssCls, cssAttr)
    self.title = title
    self.closeButton = closeButton
    self.countNotif = countNotif
    if backgroundColor:
      self.backgroundColor = backgroundColor

  def __str__(self):
    """ """
    if self.closeButton:
      items = AresItem.Item('<div class="alert %s %s notif fade in" style="top:%spx">' % (self.cssCls, 'alert-dismissable', self.countNotif * 70))
      items.add(1, '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>')
    else:
      items = AresItem.Item('<div class="alert notif %s" style="top:%spx">' % (self.cssCls, self.countNotif * 10))
    items.add(0, '<strong>%s!</strong> %s </div>' % (self.title, self.vals))
    return str(items)


class SuccessAlert(DangerAlert):
  """ """
  level = 'Success'
  backgroundColor = '#4CAF50'
  closeButton = True
  cssCls = 'alert-success'


class WarningAlert(DangerAlert):
  """ """
  level = 'Info'
  backgroundColor = '#2196F3'
  closeButton = True
  cssCls = 'alert-warning'


class InfoAlert(DangerAlert):
  """ """
  level = 'Warning'
  backgroundColor = '#ff9800'
  closeButton = True
  cssCls = 'alert-info'

