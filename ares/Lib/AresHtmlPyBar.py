"""

"""

from ares.Lib import AresHtml

class PyBar(AresHtml.HtmlItem):
  """
  Fixed Bar to allow users to download the current script or the ZIP archive of the report.
  This bar will contain for the time being the two below buttons
    - the download script button
    - the download all button

  """
  def __init__(self, htmlId, scriptEnv, scriptName, cssCls=None):
    """ Set the content of the table """
    super(PyBar, self).__init__(htmlId) # To get the HTML Id
    self.scriptName = scriptName
    self.scriptEnv = scriptEnv

  def html(self, localPath):
    """ """
    items = ['<div style="position:fixed;right:0;bottom:0;padding:3px;border:1px solid black"><img src="../../static/images/py.bmp">']

    obj = AresHtml.ButtonDownload('d_script')
    obj.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': scriptEnv, 'script': scriptName})
    items.append(obj.html(localPath))

    obj = AresHtml.ButtonDownloadAll('d_all', '').html(localPath)
    obj.js('click', "window.location.href='../download/%s/package'" % obj.http['SCRIPTS_NAME'])
    items.append(obj)
    items.append('</div>')
    return "\n".join(items)

  def js(self, evenType, jsDef):
    """
    """
    #self.jsEvent.append(('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': scriptEnv, 'script': scriptName}))
