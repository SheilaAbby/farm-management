document.addEventListener("DOMContentLoaded", function () {


   // Get the search link and results div
   const searchLink = document.getElementById('search-link');
   const searchSectionDiv = document.getElementById('search-section');

   // Add a click event listener to the search link
   searchLink.addEventListener('click', function (event) {
       // Prevent the default link behavior
       event.preventDefault();

       // Toggle the visibility of the search results div
       if (searchSectionDiv.style.display === 'none') {
        searchSectionDiv.style.display = 'block';
       } else {
        searchSectionDiv.style.display = 'none';
       }
   });
 
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
 });



  
  