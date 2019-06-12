/* jshint esversion: 6 */
import clusterData from '../map-data/cluster.geojson';
import clusterBoundaryData from '../map-data/cluster_boundary.geojson';
import edgeData from '../map-data/edges.geojson';
import nodeData from '../map-data/nodes.geojson';

var blankStyle = {
  "version": 8,
  "name": "Blank",
  "center": [
    0,
    0
  ],
  "zoom": 0,
  "sources": {},
  "sprite": "https://rawgit.com/lukasmartinelli/osm-liberty/gh-pages/sprites/osm-liberty",
  "glyphs": "https://orangemug.github.io/font-glyphs/glyphs/{fontstack}/{range}.pbf",
  "layers": [
    {
      "id": "background",
      "type": "background",
      "paint": {
        "background-color": "rgba(255,255,255,1)"
      }
    }
  ],
  "id": "blank"
};

// mapboxgl.accessToken = 'pk.eyJ1IjoiYmhlcnIyIiwiYSI6ImNqdm1wcmlhaTFmem80OGw2d3I3a2tnZGsifQ.ALfxSV65d_YJTGH5sVO4UA';
var map = new mapboxgl.Map({
    container: 'map',
    style: blankStyle,
    center: [-0, 0],
    zoom: 1,
    renderWorldCopies: false
});

map.on('load', function () {
    map.addLayer({
      "id": "cluster",
      "type": "fill",
      "source": { "type": "geojson", "data": clusterData },
      "layout": { },
      "paint": {
        "fill-color": ['get', 'fill'],
        "fill-opacity": 0.7,
        "fill-outline-color": ['get', 'stroke'],
      },
    });

    map.addLayer({
      "id": "cluster_boundary",
      "type": "line",
      "minzoom": 3,
      "source": { "type": "geojson", "data": clusterBoundaryData },
      "layout": { },
      "paint": {
        "line-color": ['get', 'stroke'],
        "line-width": 0.5,
        "line-opacity": 0.8
      },
    });

    map.addLayer({
      "id": "edges",
      "type": "line",
      "minzoom": 4,
      "source": { "type": "geojson", "data": edgeData },
      "layout": { },
      "paint": { 
        "line-color": ['get', 'stroke'],
        "line-width": 1,
        "line-opacity": 0.9
      },
    });

    map.addLayer({
      "id": "nodes",
      "type": "circle",
      "minzoom": 6,
      "source": { "type": "geojson", "data": nodeData },
      "layout": { },
      "paint": {
        "circle-color": "black",
        "circle-radius": 3
      },
    });

    map.addLayer({
      "id": "cluster-labels",
      "type": "symbol",
      "minzoom": 2,
      "source": { "type": "geojson", "data": clusterData },
      "layout": {
        "text-field": "{label}",
        "text-font": [
          "Roboto Regular"
        ],
        "text-max-width": 5,
        "text-size": 12,
        "text-anchor": "center",
        "text-radial-offset": 1
      },
      "paint": { },
    });

    map.addLayer({
      "id": "node-labels",
      "type": "symbol",
      "minzoom": 7,
      "source": { "type": "geojson", "data": nodeData },
      "layout": {
        "text-field": "{label}",
        "text-font": [
          "Roboto Regular"
        ],
        "text-max-width": 5,
        "text-size": 12,
        "text-anchor": "left",
        "text-radial-offset": 1
      },
      "paint": { },
    });

    addPopupOnClick(map, 'nodes', 'label');
    addPopupOnClick(map, 'edges', 'label');
});

function addPopupOnClick(map, layer, field) {
  // When a click event occurs on a feature in the places layer, open a popup at the
  // location of the feature, with description HTML from its properties.
  map.on('click', layer, function (e) {
    let description = e.features[0].properties[field];
    new mapboxgl.Popup()
      .setLngLat(e.lngLat)
      .setHTML(description)
      .addTo(map);
  });
  
  // Change the cursor to a pointer when the mouse is over the places layer.
  map.on('mouseenter', layer, function () {
    map.getCanvas().style.cursor = 'pointer';
  });
  
  // Change it back to a pointer when it leaves.
  map.on('mouseleave', layer, function () {
    map.getCanvas().style.cursor = '';
  });
}