
document.addEventListener("DOMContentLoaded", function () {

    // Define the data attribute that your elements share
    var dataAttribute = "data-bs-toggle";
  
    // Define the common data attribute and values to select
    var valuesToSelect = ["popover1", "popover2"];
  
    // Create an array to store the selected elements
    var popoverTriggerList = [];
  
    // Loop through the values and select the matching elements
    valuesToSelect.forEach(function (value) {
      var selector = `[${dataAttribute}="${value}"]`;
      var elements = document.querySelectorAll(selector);
      popoverTriggerList = popoverTriggerList.concat(Array.from(elements));
    });
  
    // Initialize the popovers for the selected elements
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });
  
    // Event listener for when a popover is shown
    document.body.addEventListener("shown.bs.popover", function (e) {
      var shownPopover = e.target;
  
      // Close other popovers
      popoverList.forEach(function (popover) {
        if (popover._element !== shownPopover) {
          // Close the popover by hiding it
          popover.hide();
        }
      });
    });
      // Code for location-related functionality
const locationCoordinatesInput = document.getElementById('location-coordinates');
const getLocationButton = document.getElementById('get-location-btn');

getLocationButton.addEventListener('click', function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const locationCoordinates = `${latitude}, ${longitude}`;

            locationCoordinatesInput.value = locationCoordinates;
        }, function (error) {
            console.error('Error getting location:', error.message);
        });
        } else {
            console.error('Geolocation is not supported by this browser.');
        }
    });

function togglePasswordVisibility(passwordId1, passwordId2) {
  var passwordInput1 = document.getElementById(passwordId1);
  var passwordInput2 = document.getElementById(passwordId2);

  passwordInput1.type = passwordInput1.type === "password" ? "text" : "password";
  passwordInput2.type = passwordInput2.type === "password" ? "text" : "password";
}
   });
  
  