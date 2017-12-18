""" Dedicated module to manage to load of bespoke input files
@author: Olivier Nogues

"""

import io
import zipfile

from ares.Lib import AresHtml
from flask import render_template_string


class jsFile(AresHtml.Html):
  """ Load a file on the javascript part

  File will be stored in a javascript variable and the component will have to deal with this object
  """
  delimiter = '\\t'

  def __str__(self):
    """

    :return: Return the HTML representation of this component
    """
    self.aresObj.jsGlobal.add("%s" % self.htmlId)
    self.aresObj.jsOnLoadFnc.add('''
        function handleFileSelect(evt) {
        var files = evt.target.files; var output = [];
        for (var i = 0, f; f = files[i]; i++) {
          output.push('<strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                      f.size, ' bytes, last modified: ',
                      f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a');}
        var reader = new FileReader();reader.onload = function(e) {
        displayContents(e.target.result); }; reader.readAsText(files[0]);
        document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';}

      function displayContents(contents) {
        var element = document.getElementById('file-content');
        %(htmlId)s = [] ;
        var lines = contents.split("\\n") ;
        for(var line = 0; line < lines.length; line++){%(htmlId)s.push(lines[line].split("%(delimiter)s")) ;}
        }
      document.getElementById('%(htmlId)s').addEventListener('change', handleFileSelect, false);
    ''' % {'htmlId': self.htmlId, 'delimiter': self.delimiter})
    return '<input type="file" %s name="files[]" /><output id="list"></output>' % self.strAttr()


class DownloadZip(AresHtml.Html):
  """
  """
  alias, cssCls = 'anchorFiles', ['btn', 'btn-success']
  references = []
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = []
  file_location = 'data'

  def __init__(self, aresObj, vals, fileName, cssCls=None, cssAttr=None):
    super(DownloadZip, self).__init__(aresObj, vals,  cssCls, cssAttr)
    self.fileName = fileName

  def __str__(self):
    """ The HTLM object representation """
    url = render_template_string('''{{ url_for(\'ares.downloadOutputs\', report_name=\'%s\', file_name=\'%s\', file_location=\'%s\') }}''' % (self.aresObj.reportName, self.fileName, self.file_location))
    return '<a href="%s" %s>%s</a>' % (url, self.strAttr(), self.vals)


class DownloadMemoryZip(AresHtml.Html):
  """

  TODO Find a way to send the in memory file form a report: data: %(archive)s,
  """
  alias, cssCls = 'anchorFMemory', ['btn', 'btn-success']
  references = ['https://newseasandbeyond.wordpress.com/2014/01/27/creating-in-memory-zip-file-with-python/']
  reqCss = ['bootstrap', 'font-awesome']
  file_location = 'data'

  def __init__(self, aresObj, vals, fileName, cssCls=None, cssAttr=None):
    super(DownloadMemoryZip, self).__init__(aresObj, vals,  cssCls, cssAttr)
    self.fileName = fileName
    self.memory_file = io.BytesIO()
    self.zf = zipfile.ZipFile(self.memory_file, mode='w', compression=zipfile.ZIP_DEFLATED)

  def add(self, data, filename):
    """ Add the content of string to a file in the in-memory package

    :param data: The data
    :param filename: The filename
    :return:
    """
    self.zf.writestr(filename, data)

  def namelist(self):
    """ Return the list of files in the in-memory zip archive

    :return:
    """
    return self.zf.namelist()

  def __str__(self):
    """ The HTML object representation """
    url = render_template_string('''{{ url_for(\'ares.downloadMemory\') }}''')
    self.aresObj.jsOnLoadFnc.add('''
        $('#%(htmlId)s').click(function() {
            $.ajax({
              url: %(url)s,
              type: "POST",
              contentType: attr( "enctype", "multipart/form-data" ),
              data: %(archive)s,
              success: success
            });
        });
      ''' % {'htmlId': self.htmlId, 'url': url, 'archive': self.zf})
    return '<button %s>%s</button>' % (self.strAttr(), self.vals)