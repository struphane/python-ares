#
# class Notification(object):
#   """ """
#   def __init__(self, htmlId):
#     """ """
#     self.__htmlId = htmlId
#
#   @property
#   def htmlId(self):
#     return self.__htmlId

from ares.Lib import AresHtml

class DangerAlert(AresHtml.HtmlItem):
  """ """

  level = 'Danger'
  backgroundColor = '#f44336'
  closeButton = False
  cssCls = 'alert-danger'
  jsEvent = None

  def __init__(self, htmlId, title, value, closeButton=False, backgroundColor=None, cssCls=None):
    """ """

    if cssCls:
      self.cssCls = cssCls
    super(DangerAlert, self).__init__(htmlId, self.cssCls)
    self.title = title
    self.val = value
    self.closeButton = closeButton
    if backgroundColor:
      self.backgroundColor = backgroundColor


  def html(self, localPath):
    """ """
    if self.closeButton:
      item = ['<div class="alert %s %s fade in">' % (self.cssCls, 'alert-dismissable')]
      item.append('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>')
    else:
      item = ['<div class="alert %s">' % self.cssCls]
    item.append('<strong>%s!</strong> %s </div>' % (self.title, self.val))
    return '\n'.join(item)


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

