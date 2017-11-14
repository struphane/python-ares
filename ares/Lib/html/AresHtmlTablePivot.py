from ares.Lib import AresHtml
import json

class TablePivot(AresHtml.Html):
  reqJs = ["pivot"]
  reqCss = ["pivot"]

  __dataStr, __rowStr, __colStr, __rendererName, __aggregatorName, __valStr = "", "", "", "Table", "Count", ""
  __jsFncTmpl = '''    $(function(){
        $("#%s").pivotUI(
            [
              {%s}
            ],
            {
                rows: [%s],
                cols: [%s],
                renderers: $.extend(
                        $.pivotUtilities.renderers,
                        $.pivotUtilities.d3_renderers,
                        $.pivotUtilities.export_renderers
                        ),
                rendererName: "%s",
                aggregatorName: "%s",
                vals: [%s]
            }
        );
     });
     '''

  def __init__(self, aresObj, headerBox, vals, header=None, dataFilters=None, cssCls=None, cssAttr=None):
    super(TablePivot, self).__init__(aresObj, [], cssCls, cssAttr)
    self.__dataStr = "}, {".join([",".join(['%s:"%s"' % (k, v) for k, v in rec.items()]) for rec in vals])
    self.jsEventFnc["pivot"] = {self.__jsFncTmpl % (self.htmlId, self.__dataStr, self.__colStr, self.__rowStr, self.__rendererName, self.__aggregatorName, self.__valStr)}

  def __str__(self):
    return '<div id="%s"></div>' % self.htmlId

  def setCols(self, cols=[]):
    self.__colStr = '"%s"' % '", "'.join(cols)
    self.jsEventFnc["pivot"] = {self.__jsFncTmpl % (self.htmlId, self.__dataStr, self.__colStr, self.__rowStr, self.__rendererName, self.__aggregatorName, self.__valStr)}

  def setRows(self, cols=[]):
    self.__rowStr = '"%s"' % '", "'.join(cols)
    self.jsEventFnc["pivot"] = {self.__jsFncTmpl % (self.htmlId, self.__dataStr, self.__colStr, self.__rowStr, self.__rendererName, self.__aggregatorName, self.__valStr)}

  def setRendererName(self, rendererName):
    if rendererName not in ["Table", "Table Barchart", "Heatmap", "Row Heatmap", "Col Heatmap", "Treemap"]:
      raise KeyError("rendererName not found")
    self.__rendererName = rendererName
    self.jsEventFnc["pivot"] = {self.__jsFncTmpl % (self.htmlId, self.__dataStr, self.__colStr, self.__rowStr, self.__rendererName, self.__aggregatorName, self.__valStr)}

  def setAggFun(self, aggFun):
    self.__aggregatorName, vals = aggFun
    if isinstance(vals, list):
      self.__valStr = '"%s"' % '", "'.join(vals)
    else:
      self.__valStr = '"%s"' % vals
    self.jsEventFnc["pivot"] = {self.__jsFncTmpl % (self.htmlId, self.__dataStr, self.__colStr, self.__rowStr, self.__rendererName, self.__aggregatorName, self.__valStr)}
