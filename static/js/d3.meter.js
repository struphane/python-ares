/*
  Ares unique components
*/

function meter(id, value, r, width, color) {
  // Params
  if(id === undefined || value === undefined)
    return undefined;

  //r = r || document.getElementById(id).clientWidth * .98;
  r = r || 128;
  width = width || (r / 5);
  // To change the color with the value
  if (value > 0.5)
    color = color || 'green';
  else
    color = color || '#ee7777';

  // Initial settings
  var meter_obj = {
    id: id,
    r: r,
    width: width,
    color: color,
    value: value
  };

  // Methods
  var meter_make_arc = (function() {
    var theta0 = -Math.PI / 2;
    var val = this.value * 2 * Math.PI;

    return (d3.arc || d3.svg.arc)()
      .innerRadius(this.r - width)
      .outerRadius(this.r)
      .startAngle(theta0)
      .endAngle(theta0 + val);
  }).bind(meter_obj);

  var meter_make_label = (function() {
    return (this.value * 100).toString().split('.')[0] + '%';
  }).bind(meter_obj);

  var meter_update = (function() {
    var s = d3.select('#' + this.id + ' .ares-meter-arc');
    var t = d3.select('#' + this.id + ' .ares-meter-text');

    s
      .attr('d', this.make_arc())
      .attr('fill', this.color);

    t.text(this.make_label());
  }).bind(meter_obj);

  meter_obj.make_arc = meter_make_arc;
  meter_obj.update = meter_update;
  meter_obj.make_label = meter_make_label;

  // UI
  var s = d3.select('#' + id).append('svg')
    .attr('class', 'ares-meter')
    .attr('style', 'width: ' + 2.1 * r + 'px; height: ' + 2.1 * r + 'px')
    .append('g');


  s
    .append('path')
    .attr('class', 'ares-meter-arc')
    .attr('transform', 'translate(' + r + ', ' + r + ')');

  s
    .append('text')
    .attr('class', 'ares-meter-text')
    .attr('text-anchor', 'middle')
    .attr('alignment-baseline', 'middle')
    .attr('x', r)
    .attr('y', r);

  meter_obj.update();

  return meter_obj;
}
