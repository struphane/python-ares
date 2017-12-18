""" Dedicated module to manage to load of bespoke input files
@author: Olivier Nogues

"""

from ares.Lib import AresHtml


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
