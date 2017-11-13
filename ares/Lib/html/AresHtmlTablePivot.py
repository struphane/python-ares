from ares.Lib import AresHtml
import json

class TablePivot(AresHtml.Html):
  reqJs = ["pivot"]
  reqCss = ["pivot"]

  def __init__(self, aresObj, headerBox, vals, header=None, dataFilters=None, cssCls=None, cssAttr=None):
    super(TablePivot, self).__init__(aresObj, [], cssCls, cssAttr)

    dataStr = "}, {".join([",".join(['%s:"%s"' % (k, v) for k, v in rec.items()]) for rec in vals])
    print(dataStr)

    self.jsEventFnc["pivot"] = {'''    $(function(){
        $("#%s").pivotUI(
            [
              {%s}
            ],
            {
                rows: [],
                cols: []
            }
        );
     });
     ''' % (self.htmlId, dataStr)}


  def __str__(self):
    return '<div id="%s"></div>' % self.htmlId
