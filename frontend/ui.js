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
