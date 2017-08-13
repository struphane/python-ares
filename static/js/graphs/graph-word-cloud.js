
d3.layout.cloud().size([960, 600])
    .words(data_%s) // Refer to the data variable
    .rotate(function() { return ~~(Math.random() * 2) * 90; })
    .font("Impact")
    .fontSize(function(d) { return d.size; })
    .on("end", draw)
    .start();

function draw(words) {
d3.select("#chart%s svg") // Refer to the chart variable
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
};