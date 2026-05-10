function showMap(id, lat, long, label) {
    const mapLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });
    const satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://esri.com">ESRI</a>'
    });
    const map = L.map(id, {
      layers: [mapLayer],
      center: [lat, long],
      zoom: 14,
      scrollWheelZoom: false,
    });
    const markerLayer = L.marker([lat, long]).addTo(map).bindPopup(label);
    L.control.layers({Map: mapLayer, Satellite: satLayer}, {Markers: markerLayer}).addTo(map);
  }
  document.addEventListener("DOMContentLoaded", (event) => {
    showMap('myMap', -33.865143, 151.209900, 'Sydney, Australia');
  });
