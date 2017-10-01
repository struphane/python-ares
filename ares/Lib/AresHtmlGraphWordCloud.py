""" Python Chart module to wrap the Work Cloud object

"""

from ares.Lib import AresHtmlContainer
from ares.Lib import AresItem

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
    res.append("var data_%s = buildCountRecordSet() ; " % (self.htmlId))
    res.append('''
          d3.layout.cloud().size([960, 600])
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
          }
          ;

          %s
        '''% (self.htmlId, self.htmlId, self.htmlId, self.htmlId, self.jsUpdate()))
    self.jsEvent['addGraph'] = "\n".join(res)
    return "\n".join(res)

  def jsUpdate(self):
    """ This function allow different component to update the world Cloud chart

    For example:

    """

    return '''
          // words should be the javascript version of the data set expected by the graph
          // Should be the select to the svg component
          function drawCloudUpdate(words, jsGraphRef){
             d3.layout.cloud().size([500, 500])
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .start();

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
          '''

  def __str__(self):
    """ Return the String representation of a DIV containing a SVG tag """
    self.selectCategory()
    self.selectValues()
    self.selectKey()
    self.selectSeries()

    item = AresItem.Item('')
    item.add(1, '<div style="width:95%%;height:100%%;" %s>' % self.strAttr())
    #TODO put a better display for this section
    item.add(1, '<div class="container">')
    # Add the pointers for the display
    if self.categories is not None:
      item.join(self.categories)
    if self.values is not None:
      item.join(self.values)
    if self.seriesKey is not None:
      item.join(self.seriesKey)
    if self.series is not None:
      item.join(self.series)
    item.add(1, '</div>')
    item.add(1, '<svg style="width:100%;height:400px;"></svg>')
    item.add(0, '</div>')
    item = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox)
    self.js()
    return str(item)

  def selectKey(self):
    """ for multicharts, define the key to be used in js recordSet"""
    item = AresItem.Item('')
    item.add(2, '<script>')
    for headerLine in self.header:
      if  headerLine.get('type') == 'series':
        item.add(3, "var serie_%s = '%s';" % (self.htmlId, headerLine.get('key', headerLine['colName'])))
        self.hasSeries = True
        break

    else:
      item.add(3, "var serie_%s = '';" % self.htmlId)
    item.add(2, '</script>')
    self.seriesKey = item