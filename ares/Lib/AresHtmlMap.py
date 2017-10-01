import os
import json

from ares.Lib import AresHtml, AresItem
from flask import render_template_string


class Map(AresHtml.Html):
  cssCls, alias = 'ares-map', 'map'
  reference = 'https://www.vincentbroute.fr/mapael'
  reqJs = ['mapael']

  def __init__(self, aresObj, cssCls=None):
    super(Map, self).__init__(aresObj, None, cssCls)

    self.areas = {}
    self.mapname = 'world_countries'
    self.defaultarea = {}

    # Be sure to include map JS files only once
    if not hasattr(aresObj, 'maps_included'):
      setattr(aresObj, 'maps_included', set())

  def set_default_area(self, cfg):
    slf.defaultarea = dict(cfg)

  def update_areas(self, areas):
    self.areas.update(areas)

  def __str__(self):
    item = AresItem.Item(None, self.incIndent)
    container_id = 'map-container-%s' % id(self)

    cfg = json.dumps({
      'map': { 'name': self.mapname },
      'areas': self.areas,
      'defaultarea': self.defaultarea
    })

    script = ''' $('#%s').mapael(%s); ''' % (container_id, cfg)

    if self.mapname not in self.aresObj.maps_included:
      self.aresObj.maps_included.add(self.mapname)
      item.add(0, render_template_string('''<script type="application/javascript" src="{{ url_for('static', filename='maps/%s.min.js') }}"></script>''' % self.mapname))
    item.add(0, '<div id="%s" style="width: 100%%">' % container_id)
    item.add(1, '<div class="map">Sorry, no map available</div>')
    item.add(0, '</div>')
    item.add(0, '<script>')
    item.add(1, script)
    item.add(0, '</script>')

    return str(item)
