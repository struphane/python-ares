"""

"""

from ares.Lib import AresHtml

class PyBar(object):
  """
  Fixed Bar to allow users to download the current script or the ZIP archive of the report.
  This bar will contain for the time being the two below buttons
    - the download script button
    - the download all button

  """

  def html(self, localPath):
    """ """
    items = ['<div style="position:fixed;right:0;bottom:0;padding:3px;border:1px solid black"><img src="../../static/images/py.bmp">']
    items.append(AresHtml.ButtonDownload('d_script').html(localPath))
    items.append(AresHtml.ButtonDownloadAll('d_all', '').html(localPath))
    items.append('</div>')
    return "\n".join(items)