const key = '';
    const map = L.map('myMap').setView([-33.865143, 151.209900], 14); //starting position
    L.tileLayer(`https://api.maptiler.com/maps/streets-v4/{z}/{x}/{y}.png?key=${key}`,{ //style URL
    tileSize: 512,
    zoomOffset: -1,
    minZoom: 1,
    attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
    crossOrigin: true
    }).addTo(map);

const fuelIcon = L.divIcon({
    html: '⛽',
    className: 'fuel-marker',
    iconSize: [30, 30],
    iconAnchor: [15, 10]
});

L.marker([-33.865143, 151.209900], {icon: fuelIcon})
    .addTo(map)
    .bindPopup("Sydney");
