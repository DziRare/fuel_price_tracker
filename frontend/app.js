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

const fuelTypes = document.querySelector('.fuel-types');
const mask = document.querySelector('.fuel-types-mask');
const scrollLeftBtn = document.querySelector('.scroll-left');
const scrollRightBtn = document.querySelector('.scroll-right');

const SCROLL_AMOUNT = 200; // pixels to scroll per click

scrollLeftBtn.addEventListener('click', () => {
    fuelTypes.scrollBy({ left: -SCROLL_AMOUNT, behavior: 'smooth' });
});

scrollRightBtn.addEventListener('click', () => {
    fuelTypes.scrollBy({ left: SCROLL_AMOUNT, behavior: 'smooth' });
});

function updateFades() {
    const scrollLeft = fuelTypes.scrollLeft;
    const maxScroll = fuelTypes.scrollWidth - fuelTypes.clientWidth;
    
    // Show left fade if not at the start
    mask.classList.toggle('show-left-fade', scrollLeft > 0);
    
    // Show right fade if not at the end (with a 1px tolerance for rounding)
    mask.classList.toggle('show-right-fade', scrollLeft < maxScroll - 1);
}

// Update on scroll
fuelTypes.addEventListener('scroll', updateFades);

// Update on initial load (in case content already overflows)
updateFades();

// Update on window resize (the overflow situation might change)
window.addEventListener('resize', updateFades);
