""" Python Chart module to wrap the Work Cloud object

"""

from ares.Lib.html import AresHtmlContainer
from ares.Lib import AresItem
from ares.Lib import AresJs

class WordCloud(AresHtmlContainer.GraphSvG):
  """

  This module will require the javascript module: d3.layout.cloud.js

  TODO finalise the update method and make it generic with all the graph
  the update method should appear once and only once in the javascript section of the page
  """
  mockData = r'json\pie.json'
  alias = 'cloud'
  reqJs = ['cloud']

  def js(self):
    """ Return the entries to be added to the Javascript to create the graph during the loading """
    res = ["var fill = d3.scale.category20();"]
    #res.append("var data_%s = buildCountRecordSet(%s, %s, %s, %s, %s) ;" % (self.jqRecordSet, self.jqSeriesKey, self.jqCategory, self.jqValue, self.jqSeries))
    res.append("var data_%s = buildCountRecordSet(%s, %s.val()) ; " % (self.htmlId, self.jqRecordSet, self.jqCategory))
    res.append('''
          d3.layout.cloud().size([1200, 400])
            .words(data_%s) // Refer to the data variable
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .fontSize(function(d) { return d.size; })
            .on("end", draw_%s)
            .start()
          ;

          function draw_%s(words) {
            d3.select("#%s svg") // Refer to the chart variable
              .append("g")
              .attr("transform", "translate(150,150)")
              .selectAll("text")
              .data(words)
              .enter().append("text")
              .style("font-size", function(d) { return d.size + "px"; })
              .style("font-family", "Impact")
              .style("fill", function(d, i) {  return fill(i); })
              .attr("text-anchor", "middle")
              .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
              .text(function(d) {  return d.text; });
          } ;

          function drawCloudUpdate(words, jsGraphRef){
             jsGraphRef
                .selectAll("g").attr("transform", "translate(150,150)")
                .selectAll("text")
                  .data(words).enter().append("text")
                  .style("font-size", function(d) { return d.size + "px"; })
                  .style("font-family", "Impact")
                  .style("fill", function(d, i) { return fill(i); })
                  .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";  })
                  .text(function(d) { return d.text; });
          };
        '''% (self.htmlId, self.htmlId, self.htmlId, self.htmlId))
    self.jsEvent['addGraph'] = "\n".join(res)
    return "\n".join(res)

  def selectCategory(self):
    """ Return the category to be selected in the graph display """
    style = 'style="margin-bottom:5px"' if len(self.header) > 2 else 'style="display:none"'
    item = AresItem.Item('<select id="%s_col_selector" class ="form-control input-sm" %s>' % (self.htmlId, style))
    item.add(1, '<optgroup label="X-Axis">')
    for headerLine in self.header:
      if headerLine.get('type') != 'object':
        if headerLine.get('selected') and headerLine.get('type') != 'number':
          item.add(3, '<option value="%s" selected>%s</option>' % (headerLine.get('key', headerLine['colName']), headerLine['colName']))
        elif headerLine.get('type') != 'series':
          item.add(3, '<option value="%s">%s</option>' % (headerLine.get('key', headerLine['colName']), headerLine['colName']))
    item.add(2, '</select>')
    self.categories = item
    self.jsEvent['cat-change'] = AresJs.JQueryEvents("%s_col_selector" % self.htmlId,
                                                     "$('#%s_col_selector')" % self.htmlId,
                                                     'change', self.update(self.vals), '')

  def jsUpdate(self, jsDataVar='data'):
    """ This function allow different component to update the world Cloud chart

    For example:

    """

    return '''
              var filterRecordSet = buildCountRecordSet(data, %s.val()) ;

              d3.layout.cloud().size([1200, 400])
                .words(filterRecordSet) // Refer to the data variable
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .on("end", draw_new_%s)
                .start()
              ;

              function draw_new_%s(words) {
                d3.select("#%s svg g").remove();
                d3.select("#%s svg") // Refer to the chart variable
                  .append("g")
                  .attr("transform", "translate(150,150)")
                  .selectAll("text")
                  .data(words)
                  .enter().append("text")
                  .style("font-size", function(d) { return d.size + "px"; })
                  .style("font-family", "Impact")
                  .style("fill", function(d, i) {  return d3.scale.category20()(i); })
                  .attr("text-anchor", "middle")
                  .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
                  .text(function(d) {  return d.text; });
              } ;

              function drawCloudUpdate(words, jsGraphRef){
                 jsGraphRef
                    .selectAll("g").attr("transform", "translate(150,150)")
                    .selectAll("text")
                      .data(words).enter().append("text")
                      .style("font-size", function(d) { return d.size + "px"; })
                      .style("font-family", "Impact")
                      .style("fill", function(d, i) { return fill(i); })
                      .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";  })
                      .text(function(d) { return d.text; });
              };


           ''' % (self.jqCategory, self.htmlId, self.htmlId, self.htmlId, self.htmlId)

  def update(self, data):
    """ Update the content of an HTML component """
    return '''
              var filterRecordSet = buildCountRecordSet(%s, %s.val()) ;

              d3.layout.cloud().size([1200, 400])
                .words(filterRecordSet) // Refer to the data variable
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .on("end", draw_new_%s)
                .start()
              ;

              function draw_new_%s(words) {
                d3.select("#%s svg g").remove();
                d3.select("#%s svg") // Refer to the chart variable
                  .append("g")
                  .attr("transform", "translate(150,150)")
                  .selectAll("text")
                  .data(words)
                  .enter().append("text")
                  .style("font-size", function(d) { return d.size + "px"; })
                  .style("font-family", "Impact")
                  .style("fill", function(d, i) {  return d3.scale.category20()(i); })
                  .attr("text-anchor", "middle")
                  .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
                  .text(function(d) {  return d.text; });
              } ;

              function drawCloudUpdate(words, jsGraphRef){
                 jsGraphRef
                    .selectAll("g").attr("transform", "translate(150,150)")
                    .selectAll("text")
                      .data(words).enter().append("text")
                      .style("font-size", function(d) { return d.size + "px"; })
                      .style("font-family", "Impact")
                      .style("fill", function(d, i) { return fill(i); })
                      .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";  })
                      .text(function(d) { return d.text; });
              };


           ''' % (self.jqRecordSet, self.jqCategory, self.htmlId, self.htmlId, self.htmlId, self.htmlId)

  def __str__(self):
    """ Return the String representation of a DIV containing a SVG tag """
    self.selectCategory()
    item = AresItem.Item('')
    item.add(1, '<div style="width:95%%;height:100%%;" %s>' % self.strAttr())
    #TODO put a better display for this section
    item.add(1, '<div class="container">')
    if self.categories is not None:
      item.join(self.categories)
    item.add(1, '</div>')
    item.add(1, '<svg style="width:100%;height:400px;"></svg>')
    item.add(0, '</div>')
    item = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox)
    self.js()
    return str(item)
