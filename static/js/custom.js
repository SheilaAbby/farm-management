
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

  var indicator = document.getElementById("new-message-indicator");

  // checks for new messages
  $.ajax({
      url: '/check_new_message/',
      method: 'GET',
      success: function(data) {
          var hasNewMessage = data.has_new_message;
          var newMessagesCount = data.new_messages_count;
  
          if (hasNewMessage) {
              indicator.style.visibility = "visible";
              
              // Set the envelope icon and the number of new messages
              var iconText = `<i class="fas fa-envelope text-danger"></i>`;
              var messageText = `${iconText} <span class="text-danger">(${newMessagesCount})</span>`;
              
              indicator.innerHTML = messageText;
          }
      },
      error: function(error) {
          console.error('Error checking new messages!!!!:', error);
      }
  });
  

 });
