from ares.Lib import AresHtml, AresItem
from ares.Lib.html import AresHtmlContainer

class TablePivot(AresHtml.Html):
  reqJs = ["pivot"]
  reqCss = ["pivot"]

  __dataStr, __rowStr, __colStr, __rendererName, __aggregatorName, __valStr = "", "", "", "Table", "Count", ""
  __jsFncTmpl = '''
      function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      }

  
      var diffAgg = function(attributeArray) {
      
            return function(data, rowKey, colKey) {
                return {
                  key1Agg: 0,
                  key2Agg: 0,
                  push: function(record) {
                      this.key1Agg += parseFloat(record[attributeArray[0]]);
                      this.key2Agg += parseFloat(record[attributeArray[1]]);
                      },
                  value: function() {return this.key1Agg - this.key2Agg;},
                  format: function(x) {return numberWithCommas(x.toFixed(2));},
                  numInputs: 2
                };
            };
      };

      var diffPctAgg = function(attributeArray) {
      
            return function(data, rowKey, colKey) {
                return {
                  key1Agg: 0,
                  key2Agg: 0,
                  push: function(record) {
                      this.key1Agg += parseFloat(record[attributeArray[0]]);
                      this.key2Agg += parseFloat(record[attributeArray[1]]);
                      },
                  value: function() {return (this.key1Agg - this.key2Agg) / this.key1Agg;},
                  format: function(x) {return numberWithCommas(x.toFixed(2));},
                  numInputs: 2
                };
            };
      };

      var diffAbsAgg = function(attributeArray) {
      
            return function(data, rowKey, colKey) {
                return {
                  key1Agg: 0,
                  key2Agg: 0,
                  push: function(record) {
                      this.key1Agg += parseFloat(record[attributeArray[0]]);
                      this.key2Agg += parseFloat(record[attributeArray[1]]);
                      },
                  value: function() {return Math.abs(this.key1Agg - this.key2Agg);},
                  format: function(x) {return numberWithCommas(x.toFixed(2));},
                  numInputs: 2
                };
            };
      };

      var diffAbsPctAgg = function(attributeArray) {
      
            return function(data, rowKey, colKey) {
                return {
                  key1Agg: 0,
                  key2Agg: 0,
                  push: function(record) {
                      this.key1Agg += parseFloat(record[attributeArray[0]]);
                      this.key2Agg += parseFloat(record[attributeArray[1]]);
                      },
                  value: function() {return Math.abs((this.key1Agg - this.key2Agg) / this.key1Agg);},
                  format: function(x) {return numberWithCommas(x.toFixed(2));},
                  numInputs: 2
                };
            };
      };

      var sumOverSumAgg = function(attributeArray) {
      
          return function(data, rowKey, colKey) {
              return {
                key1Agg: 0,
                key2Agg: 0,
                push: function(record) {
                    this.key1Agg += parseFloat(record[attributeArray[0]]);
                    this.key2Agg += parseFloat(record[attributeArray[1]]);
                    },
                value: function() {return this.key1Agg / this.key2Agg;},
                format: function(x) {return numberWithCommas(x.toFixed(2));},
                numInputs: 2
              };
          };
      };

      var maxAgg = function(attributeArray) {
      
          return function(data, rowKey, colKey) {
              return {
                keyAgg: -Infinity,
                push: function(record) {
                        this.keyAgg = Math.max(this.keyAgg, parseFloat(record[attributeArray[0]]));
                    },
                value: function() {return this.keyAgg;},
                format: function(x) {return numberWithCommas(x.toFixed(2));},
                numInputs: 1
              };
          };
      };

      var minAgg = function(attributeArray) {
      
          return function(data, rowKey, colKey) {
              return {
                keyAgg: Infinity,
                push: function(record) {
                        this.keyAgg = Math.min(this.keyAgg, parseFloat(record[attributeArray[0]]));
                    },
                value: function() {return this.keyAgg;},
                format: function(x) {return numberWithCommas(x.toFixed(2));},
                numInputs: 1
              };
          };
      };

      var avgAgg = function(attributeArray) {
      
          return function(data, rowKey, colKey) {
              return {
                keyAgg: 0,
                cnt: 0,
                push: function(record) {
                        this.keyAgg += parseFloat(record[attributeArray[0]]);
                        this.cnt += 1;
                    },
                value: function() {return this.keyAgg / this.cnt;},
                format: function(x) {return numberWithCommas(x.toFixed(2));},
                numInputs: 1
              };
          };
      };

      $(function(){
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
                aggregators: { "Diff": diffAgg
                             , "Diff Pct": diffPctAgg
                             , "Diff Abs": diffAbsAgg
                             , "Diff Abs Pct": diffAbsPctAgg
                             , "Sum over Sum": sumOverSumAgg
                             , "Max": maxAgg
                             , "Min": minAgg
                             , "Avg": avgAgg
                             },
                aggregatorName: "%s",
                vals: [%s]
            }
        );
     });
  '''

  def __init__(self, aresObj, headerBox, vals, header=None, dataFilters=None, cssCls=None, cssAttr=None):
    super(TablePivot, self).__init__(aresObj, [], cssCls, cssAttr)
    self.headerBox = headerBox
    self.__dataStr = "}, {".join([",".join(['%s:"%s"' % (k, v) for k, v in rec.items()]) for rec in vals])
    self.jsEventFnc["pivot"] = {self.__jsFncTmpl % (self.htmlId, self.__dataStr, self.__colStr, self.__rowStr, self.__rendererName, self.__aggregatorName, self.__valStr)}

  def __str__(self):
    item = AresItem.Item(None, self.incIndent)
    item.add(0, '<div %s></div>' % self.strAttr())
    if self.headerBox is not None:
      item = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox, properties=self.references)
    return str(item)

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
