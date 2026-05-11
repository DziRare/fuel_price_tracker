// Specify the API endpoint for user data
const apiUrl = 'http://127.0.0.1:8000/stations';
const myForm = document.getElementById('location-form');

myForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload

    const formData = new FormData(myForm);
    const params = new URLSearchParams(formData);   

    try {
        const response = await fetch(`${apiUrl}?${params}`);
        
        const result = await response.json();
        console.log('Success:', result);
    } catch (error) {
        console.error('Error:', error);
    }

    // for (let step = 0; step < 5; step++) {
    //     // Runs 5 times, with values of step 0 through 4.
    //     console.log("Walking east one step");
    // }

});

