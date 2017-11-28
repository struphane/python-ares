
from ares.Lib import AresHtml
from ares.Lib import AresItem
from flask import render_template_string

class FileDeployer(AresHtml.Html):
  """ HTML object for the HR tags """
  cssCls, alias = ['deploy'], 'deploy'
  reqJs = ['ares']

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None):
    """ """
    super(FileDeployer, self).__init__(aresObj, vals, cssCls, cssAttr)
    if not aresObj.http['REPORT_NAME'].startswith('_Ares'):
        raise EnvException("You're not allowed to use this function, use the AresDeploy instead")

  def resolve(self):
    """ """
    url = render_template_string(''' {{ url_for(\'ares.testDeploy\') }} ''')
    return url

  def __str__(self):

    url = self.resolve()

    item = AresItem.Item("""<form action="%s" method="POST" enctype="multipart/form-data" >"""  % url)
    item.add(1, """<div style="padding-top:3px" id="%s">""" % self.htmlId)
    item.add(2, """<br><input type="file" name="file" />
            <select name="File Type" required> """ )
    item.add(3, """ <option value="report">report</option>""")
    item.add(3, """ <option value="configuration">configuration</option>""")
    item.add(3, """ <option value="ajax">ajax</option>""")
    item.add(3, """ <option value="javascript">javascript</option>""")
    item.add(3, """ <option value="views">views</option>""")
    item.add(3, """ <option value="outputs">outputs</option>""")
    item.add(3, """ <option value="styles">styles</option>""")
    item.add(3, """ <option value="saved">saved</option>""")
    item.add(2, """ </select>""")
    item.add(1, """ </div>""")
    item.add(1, """ <button type="button" class="btn-xs fa fa-plus" onClick="addInputForUpload('%s');"></button><br>""" %(self.htmlId))
    item.add(1, """ <br><input type="submit"/>""")
    item.add(0, """ <form/>""")
    return str(item)


class FileUploader(AresHtml.Html):
  """ HTML object for the HR tags """
  cssCls, alias = ['upload'], 'upload'
  reqJs = ['ares']

  def resolve(self):
    """ """
    url = render_template_string(''' {{ url_for(\'ares.uploadSingleFile\', report_name=\'%s\') }} ''' % self.aresObj.http['REPORT_NAME'])
    return url

  def __str__(self):

    url = self.resolve()

    item = AresItem.Item("""<form action="%s" method="POST" enctype="multipart/form-data" >"""  % url)
    item.add(1, """<div style="padding-top:3px" id="%s">""" % self.htmlId)
    item.add(2, """<br><input type="file" name="file" /> """ )
    item.add(1, """ </div>""")
    item.add(1, """ <button type="button" class="btn-xs fa fa-plus" onClick="addInputforDeploy('%s');"></button><br>""" %(self.htmlId))
    item.add(1, """ <br><input type="submit"/>""")
    item.add(0, """ <form/>""")
    return str(item)


