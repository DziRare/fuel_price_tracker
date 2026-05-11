// Specify the API endpoint for user data
const apiUrl = 'http://127.0.0.1:8000/stations';
const myForm = document.getElementById('location-form');

// Intial map API setup
const key = 'my_map_key';
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

const markerGroup = L.layerGroup().addTo(map);

myForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload

    const formData = new FormData(myForm);
    const params = new URLSearchParams(formData);   

    try {
        const response = await fetch(`${apiUrl}?${params}`);
        
        const result = await response.json();
        console.log('Success:', result);
        markerGroup.clearLayers();

        for (let step = 0; step < result.length; step++) {
            console.log(`Name: ${result[step]["name"]}`);
            console.log(`Address: ${result[step]["address"]}`);
            console.log(`Price: ${result[step]["price"]}c`);
            console.log(`Fuel: ${result[step]["fuel_type"]}`);
            console.log(`Distance: ${result[step]["distance"]}km`);
            
            L.marker([result[step]["latitude"], result[step]["longitude"]], {icon: fuelIcon})
            .addTo(markerGroup)
            .bindPopup(`${result[step]["name"]}: $${result[step]["price"]}, ${result[step]["distance"]}km`);
        }

    } catch (error) {
        console.error('Error:', error);
    }

});
