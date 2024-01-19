// function getLocationAndSendToServer() {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(function (position) {
//             var latitude = position.coords.latitude;
//             var longitude = position.coords.longitude;

//             // Create a JavaScript object with the coordinates
//             var coordinates = { 'latitude': latitude, 'longitude': longitude };

//             // Send the coordinates to the Flask server as JSON data
//             fetch('/getdoc', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json' // Set the Content-Type header to indicate JSON data
//                 },
//                 body: JSON.stringify(coordinates) // Convert the JavaScript object to a JSON string
//             })
//             .then(response => response.json())
//             .then(data => {
//                 console.log(data.message);
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//         });
//     } else {
//         console.log("Geolocation is not supported by this browser.");
//     }
// }
    // Function to handle geolocation success
    function handleGeolocationSuccess(position) {
        const latitudeField = document.getElementById("latitude");
        const longitudeField = document.getElementById("longitude");

        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        // Fill the latitude and longitude fields
        latitudeField.value = latitude;
        longitudeField.value = longitude;
    }

    // Function to handle geolocation error
    function handleGeolocationError(error) {
        console.error("Error getting geolocation:", error);
        // You can provide a fallback or error message here if needed
    }

    // Check if geolocation is supported by the browser
    if ("geolocation" in navigator) {
        // Get the user's geolocation
        navigator.geolocation.getCurrentPosition(handleGeolocationSuccess, handleGeolocationError);
    } else {
        console.error("Geolocation is not supported by your browser.");
        // You can provide a fallback or error message here if geolocation is not supported
    }
