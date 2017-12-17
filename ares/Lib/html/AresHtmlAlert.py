""" Python Wrapper to display alerts in reports
@author: Olivier Nogues

"""


from ares.Lib import AresHtml


class DangerAlert(AresHtml.Html):
  """

  """
  level, cssCls = 'Danger', ['alert-danger']
  backgroundColor = '#f44336'
  closeButton = False
  reqJs, reqCss = ['bootstrap'], ['bootstrap']

  def __init__(self, aresObj, title, value, countNotif, closeButton=False, backgroundColor=None, cssCls=None, cssAttr=None):
    """ Instantiate the Danger notification box """
    super(DangerAlert, self).__init__(aresObj, value, self.cssCls, cssAttr)
    self.title = title
    self.closeButton = closeButton
    self.countNotif = countNotif
    if backgroundColor:
      self.backgroundColor = backgroundColor

  def __str__(self):
    """ Return the string representation for an alert """
    if self.closeButton:
      item = ['<div class="alert %s %s notif in" style="top:%spx; z-index:300;right:5px;width:400px">' % (" ".join(self.attr['class']), 'alert-dismissable', 50 + self.countNotif * 70)]
      item.append('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>')
    else:
      item = ['<div class="alert notif %s" style="top:%spx; z-index:300;right:5px;width:300px">' % (" ".join(self.attr['class']), 50 + self.countNotif * 10)]
    item.append('<strong>%s!</strong> %s </div>' % (self.title, self.vals))
    return "".join(item)


class SuccessAlert(DangerAlert):
  """ """
  level = 'Success'
  backgroundColor = '#4CAF50'
  closeButton = True
  cssCls = ['alert-success']


class WarningAlert(DangerAlert):
  """ """
  level = 'Info'
  backgroundColor = '#2196F3'
  closeButton = True
  cssCls = ['alert-warning']


class InfoAlert(DangerAlert):
  """ """
  level = 'Warning'
  backgroundColor = '#ff9800'
  closeButton = True
  cssCls = ['alert-info']

