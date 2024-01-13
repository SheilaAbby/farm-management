// Function to get CSRF token from cookies
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

// Function to get the current user
let currentUserCache = null;

async function fetchCurrentUser() {
    try {
        // Check if user data is already in the cache
        if (currentUserCache) {
            return currentUserCache.user;
        }

        // Fetch the CSRF token
        var csrftoken = getCookie('csrftoken');

        // Make an AJAX request to get the current user
        const response = await fetch('/get_current_user/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            credentials: 'include',  // Include credentials (cookies) in the request
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json(); //returns an object with user property

        // Cache the current user data
        currentUserCache = data;
        
        // Reset the cache after a certain period (e.g., 30 minutes)
        setTimeout(() => {
            currentUserCache = null;
        }, 30 * 60 * 1000);

        return data.user || null; // Return null if user data is not available
    } catch (error) {
        console.error('Error fetching current user:', error);
        console.error('Error details:', error.message, error.stack);
        return null;
    }
}

let isFetching = false;

async function getCurrentUser() {
    try {
      
        // Set isFetching to true to prevent subsequent requests
        isFetching = true;

        const startTimestamp = Date.now();
        const data = await fetchCurrentUser(); //here data is the actual user object
        const endTimestamp = Date.now();

        // Calculate the time taken by the asynchronous call
        const timeTaken = endTimestamp - startTimestamp;

        // Adjust the delay based on the time taken, with a minimum delay
        const delay = Math.max(0, 10000 - timeTaken);

        // Reset isFetching after the adjusted delay
        setTimeout(() => {
            isFetching = false;
        }, delay);

        return data;
    } catch (error) {

        console.error('Error fetching current user:', error);
        console.error('Error details:', error.message, error.stack);

        // Reset isFetching immediately on error
        isFetching = false;

        return null;
    }
}

// Function to get the user role
async function getUserRole() {
    try {
        // Ensure that getCurrentUser has resolved before proceeding
        var user = await getCurrentUser();

        if (user && user.groups && Array.isArray(user.groups)) {
            // Check if the user belongs to the 'field_agent' group
            if (user.groups.includes('field_agent')) {
                return 'field_agent';
            }

            // Check if the user belongs to the 'farmer' group
            if (user.groups.includes('farmer')) {
                return 'farmer';
            }
        }

        return 'unknown'; // Default to 'unknown' if the role is not defined
    } catch (error) {
        console.error('Error fetching user role:', error);
        return 'unknown';
    }
}

// Function to toggle the visibility of the delete button for a specific user
async function toggleDeleteButton(sender, messageId) {
    var deleteButton = document.getElementById('deleteButton-' + messageId);

    if (deleteButton) {

        try {
            const currentUserData = await getCurrentUser();
     
            const userRole = await getUserRole();
          
            // Check if the condition is met and log accordingly
            if (userRole === 'farmer' && sender === currentUserData.username) {
                deleteButton.classList.toggle('d-none', false);
            } else if (userRole === 'field_agent') {
                deleteButton.classList.toggle('d-none', false);
            } else {
                deleteButton.classList.toggle('d-none', true);
            }
        } catch (error) {
            console.error('Error toggling delete button:', error);
        }
    }
}

// Function to toggle the visibility of the reply delete button
async function toggleDeleteReplyButton(sender, messageId, replyId) {
    console.log('Toggle delete called with replyID ', replyId);
    console.log('Toggle delete called with sender', sender);

    try {
        const currentUserData = await getCurrentUser();
        const userRole = await getUserRole();

        // Generate the ID of the delete reply button dynamically
        var deleteReplyButtonId = `deleteReplyButton-${messageId}-${replyId}`;
        var deleteReplyButton = document.getElementById(deleteReplyButtonId);

        console.log('Reply button found here', deleteReplyButton);

        if (deleteReplyButton) {
            console.log('Reply button found', deleteReplyButton);
            // Check if the condition is met and toggle the button accordingly
            if (userRole === 'farmer' && sender === currentUserData.username) {
                console.log('Reply belongs to the user', sender);
                deleteReplyButton.classList.toggle('d-none', false);
            } else if (userRole === 'field_agent') {
                deleteReplyButton.classList.toggle('d-none', false);
            } else {
                deleteReplyButton.classList.toggle('d-none', true);
            }
        } else {
            console.error(`Reply button not found for messageId: ${messageId}, replyId: ${replyId}`);
        }
    } catch (error) {
        console.error('Error toggling delete reply button:', error);
    }
}

async function updateRepliesSection(messageId, reply) {
    var repliesSection = document.getElementById('repliesSection-' + reply);

    if (repliesSection) {
        repliesSection.classList.remove('d-none');

        // Clear existing content in the replies section
        repliesSection.innerHTML = '';

        // Fetch the original message using the reply ID
        try {
            const response = await fetch('/fetch_message_with_replies/' + reply + '/');
            const originalMessage = await response.json();
           
            // Check if there are replies in the original message object
            if (originalMessage.message.replies && originalMessage.message.replies.length > 0) {
                
                // Create an unordered list to contain the replies
                var repliesList = document.createElement('ul');
                repliesList.className = 'list-unstyled';

                // Iterate through each reply and append it to the list
                originalMessage.message.replies.forEach(function (replyItem) {
                    var replyItemElement = document.createElement('li');

                    var created = replyItem.created;

                    const created_date = new Date(created);

                    const formattedDate = `${created_date.toDateString()} ${created_date.toLocaleTimeString()} (EAT)`;

                   // replyItemElement.innerHTML = '<span style="font-weight: bold;">' + replyItem.sender + ':</span> ' + replyItem.content;

                    replyItemElement.innerHTML = `
                    <div id="reply-${replyItem.id}" data-created="${replyItem.created}">
                        <span style="margin-left: 30px;">
                            <i class="fas fa-comments text-success"></i>
                            <span style="font-weight: bold; margin-left: 0.5rem;">${replyItem.sender}: </span>
                            <span style="color: #975344; margin-left: 0.5rem;">replied...</span>
                            <span style="color: green;">${replyItem.content}</span>
                            - sent on ${formattedDate}
                            <button class="btn btn-sm ms-2" onclick="deleteReply(${messageId}, ${reply.id})" id="deleteReplyButton-${messageId}-${reply.id}" style="color: #975344;">
                            <i class="material-icons small">delete</i>
                            </button>
                        </span>
                    </div>
                    `;
                    repliesList.appendChild(replyItemElement);
                });

                // Append the list of replies to the replies section
                repliesSection.appendChild(repliesList);
            } else {
                // If there are no replies, display a message
                var noRepliesMessage = document.createElement('p');
                noRepliesMessage.textContent = 'No replies yet.';
                repliesSection.appendChild(noRepliesMessage);
            }

            // Display the reply text field and send button
            var replyField = document.createElement('textarea');
            replyField.className = 'form-control mt-3';
            replyField.placeholder = 'Reply to ' + originalMessage.message.sender + '...';
            replyField.id = 'replyField-' + reply;

            var sendButton = document.createElement('button');
            sendButton.textContent = 'Send';
            sendButton.className = 'btn btn-primary mt-2';
            sendButton.id = 'sendButton-' + reply;

            sendButton.onclick = function () {
                sendReply(originalMessage.message.sender, reply);
            };

            // Append the reply field and send button to the replies section
            repliesSection.appendChild(replyField);
            repliesSection.appendChild(sendButton);
        } catch (error) {
            console.error('Error fetching original message:', error);
        }
    } 
}

function sendReply(sender, messageId) {
    var replyField = document.getElementById('replyField-' + messageId);

    if (replyField) {
        var replyContent = replyField.value.trim();

        if (replyContent) {
            // AJAX request to save the reply
            fetch('/windwood/chatroom/' + messageId + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ content: replyContent }),
            })
                .then(response => response.json())
                .then(data => {
                    // Optionally, clear the reply field after a successful reply
                    replyField.value = '';

                    // Hide the reply field and the "Send" button
                    toggleReplyField(sender, messageId);
                    // Update the replies section with the new reply
                    updateRepliesSection(sender, messageId, data.reply);

                    // Show the success message
                    var successMessage = document.getElementById('successReply');
                    successMessage.classList.remove('d-none');

                    // Automatically remove the success message and reload the page after 3000 milliseconds (3 seconds)
                    setTimeout(function () {
                        successMessage.style.display = 'none';
                        location.reload();
                    }, 3000);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            console.error('Reply content is empty for sender:', sender);
            alert('Please write a Reply');
        }
    } else {
        console.error('Reply field not found for sender:', sender);
    }
}

// Create a "Send" button for a specific user
function createSendButton(sender, messageId) {
    const sendButton = document.createElement('button');
    sendButton.textContent = 'Send';
    sendButton.className = 'btn btn-primary mt-2 d-none';
    sendButton.id = 'sendButton-' + messageId;

    sendButton.addEventListener('click', () => sendReply(sender, messageId));

    const messageElement = latestMessages[sender];
    messageElement && messageElement.appendChild(sendButton);

    return sendButton;
}

// Dictionary to track the visibility state of reply fields and send buttons
var replyFieldsState = {};

// Dictionary to store the "Send" button for each user
var sendButtons = {};

// Function to toggle the visibility of the reply field and send button for a specific user
function toggleReplyField(sender, messageId) {

    var replyField = document.getElementById('replyField-' + messageId);
    var repliesSection = document.getElementById('repliesSection-' + messageId);

    // Initialize to false if undefined
    replyFieldsState[messageId] = replyFieldsState[messageId] || false;

    // Toggle the visibility state
    replyFieldsState[messageId] = !replyFieldsState[messageId];

    // Toggle the visibility of the reply field
    if (replyField) {
        // Toggle the 'd-none' class based on the visibility state
        replyField.classList.toggle('d-none', !replyFieldsState[messageId]);
    }

    // Toggle the visibility of the replies section
    if (repliesSection) {
        repliesSection.classList.toggle('d-none', !replyFieldsState[messageId]);

        // If the replies section is visible, focus on the reply field
        if (!repliesSection.classList.contains('d-none')) {
            replyField.focus();
        }
    }

    // Create or get the "Send" button for the specific messageId
    if (!sendButtons[messageId]) {
        sendButtons[messageId] = createSendButton(sender, messageId);
    } 

    // Toggle the visibility of the "Send" button
    if (sendButtons[messageId]) {
        sendButtons[messageId].classList.toggle('d-none', !replyFieldsState[messageId]);
    }
}

// Function to remove a message from the UI
function removeMessage(sender, messageId) {
    // Get the message element by ID and log values for debugging
    var messageElement = document.getElementById('message-' + messageId);
  
    if (messageElement) {
        // Log a confirmation message when the element is found
        messageElement.remove();
        // Remove the message from latestMessages dictionary
        delete latestMessages[sender];
    } else {
        console.error('Message element not found for messageId:', messageId);
    }
}

// Remove a reply or entire replies section from the UI
function removeReply(messageId, replyId) {
    try {
        // Get the replies section associated with the main message
        var repliesSection = document.getElementById(`repliesSection-${messageId}`);

        if (repliesSection) {
            if (replyId) {
                // If replyId is provided, find the reply element by its ID and remove it
                var replyElement = document.getElementById(`reply-${replyId}`);

                if (replyElement) {
                    replyElement.remove();
                } else {
                    console.error(`Reply element not found for reply ID ${replyId}`);
                }
            } else {
                // If replyId is not provided, remove the entire replies section
                repliesSection.remove();
                
            }
        } else {
            console.error(`Replies section not found for message ID ${messageId}`);
        }
    } catch (error) {
        console.error('Error removing reply:', error);
    }
}

function deleteMessage(sender, messageId) {
    // Check if messageId is valid
    if (!messageId) {
        console.error('Invalid messageId:', messageId);
        return;
    }

    // Show confirmation dialog
    var confirmDelete = window.confirm('Are you sure you want to delete this message?');

    if (confirmDelete) {
        // User clicked OK in the confirmation dialog

        // AJAX request to delete the message
        fetch('/windwood/chatroom/delete/' + messageId + '/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => {
            if (response.ok) {
                // If the response is OK, parse JSON response
                return response.json();
            } else {
                console.error('Error deleting message. Status:', response.status);
                throw new Error('Error deleting message.');
            }
        })
        .then(data => {
            if (data.success) {
               
                if (data.message_id) {
                    removeReply(data.message_id);
                }

                 // Remove the deleted message and its replies from the UI
                 removeMessage(sender, messageId);

                // Display a success message to the user
                alert('Message deleted successfully!');

            } else {
                console.error('Error deleting message:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    // If the user clicked Cancel, do nothing
}

function deleteReply(messageId, replyId) {
    // Check if messageId and replyId are valid
    if (!messageId || !replyId) {
        console.error('Invalid messageId or replyId:', messageId, replyId);
        return;
    }

    // Show confirmation dialog
    var confirmDelete = window.confirm('Are you sure you want to delete this reply?');

    if (confirmDelete) {
        // User clicked OK in the confirmation dialog

        // AJAX request to delete the reply
        fetch(`/windwood/chatroom/delete/${messageId}/reply/${replyId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => {
            if (response.ok) {
                // If the response is OK, parse JSON response
                return response.json();
            } else {
                console.error('Error deleting reply. Status:', response.status);
                throw new Error('Error deleting reply.');
            }
        })
        .then(data => {
            if (data.success) {
                // Remove the deleted reply from the UI
                removeReply(messageId, replyId);

                // Display a success message to the user
                alert('Reply deleted successfully!');
            } else {
                console.error('Error deleting reply:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    // If the user clicked Cancel, do nothing
}

// Function to handle user interaction with notifications
async function handleNotificationInteraction(userClickedOK, messageIds) {
    if (userClickedOK && messageIds && messageIds.flat().length > 0) {

        // Mark the messages as processed on the server
        for (const messageId of messageIds.flat()) {
            await markMessageAsProcessedOnServer(messageId);
        }
    } else {
        console.log('User canceled or did not confirm');
        // Handle the case where the user canceled or did not confirm viewing the notification
    }

    // Clear the messages array after displaying notifications
    messages = [];
}

async function displayNotification(messages, interactionCallback) {
    try {
        const currentUserData = await getCurrentUser();

        // Ensure currentUserData is resolved before proceeding
        if (currentUserData) {
      
            // Filter messages where the sender is not the current user
            const filteredMessages = messages.filter(message => message.sender !== currentUserData.username);
            
            // Ensure uniqueness of message IDs
            const uniqueMessageIds = [...new Set(filteredMessages.map(message => message.id))];
           
            const numberOfMessages = uniqueMessageIds.flat().length;

            // Display a bulk notification only once
            if (numberOfMessages > 0) {
                const userClickedOK = confirm(`You have ${numberOfMessages} new messages. Check the chat!`);
                // Call the interaction callback with unique message IDs
                interactionCallback(userClickedOK, uniqueMessageIds); // Passing unique message IDs for marking as processed if user clicks OK

                // Remove the notified messages from the messages array
                if (userClickedOK) {
                    messages = messages.filter(message => !uniqueMessageIds.includes(message.id));
                }
            }
        }
    } catch (error) {
        console.error('Error getting current user data:', error);
        // Handle error if needed
    }
}

//  Updates the Chat Container with Messages + Replies
var latestMessages = {};

function updateChatContainer(message) {

    // Get the username, content,messageId, and created timestamp from the message
    var sender = message.sender;
    var content = message.content;
    var created = message.created;
    var messageId = message.id;
    var senderPhotoUrl = message.senderPhotoUrl;

    const created_date = new Date(created);

    const formattedDate = `${created_date.toDateString()} ${created_date.toLocaleTimeString()} (EAT)`;
  
    // Check if any deletion flag is true
    if (
        message.deleted_by_sender ||
        message.deleted_for_recipients ||
        message.deleted_by_field_agent
    ) {
        return;
    }

    // Check if the user already has a message in the chat container
    if (sender in latestMessages) {
        // Update the existing message
        latestMessages[sender].innerHTML = `
            <div id="message-${messageId}" data-created="${created}">
                <div class="d-flex align-items-center">
                <img src="${senderPhotoUrl || '/media/profile_photos/blank-avatar.png'}" alt="Profile Photo" class="rounded-circle overflow-hidden me-2" style="width: 35px; height: 35px;" onerror="this.onerror=null; this.src='/media/profile_photos/avatar-user.svg';">
                <span style="font-weight: bold;">${sender}:</span>
                <span style="color: #975344; margin-left: 0.5rem;">shared...</span>
                </div>
                <span style="color: green; margin-left: 0.5rem;">${content}</span>
                - sent on ${formattedDate}
                <button class="btn btn-sm ms-2" onclick="toggleReplyField('${sender}', ${messageId})" style="color: green;">
                    <i class="material-icons small">reply</i>
                </button>
                <button class="btn btn-sm ms-2" onclick="deleteMessage('${sender}', ${messageId})" id="deleteButton-${messageId}" style="color: #975344;">
                    <i class="material-icons small">delete</i>
                </button>
            </div>
            <hr>
            <div class="replies-section mt-2 d-none" id="repliesSection-${messageId}"></div>
        `;

        // Now, append the reply field and send button separately
        var repliesSection = document.getElementById(`repliesSection-${messageId}`);
        if (repliesSection) {
            var replyField = document.createElement('textarea');
            replyField.className = 'form-control mt-2';
            replyField.placeholder = 'Reply to ' + sender + '...';
            replyField.id = 'replyField-' + messageId;

            // Append the reply field to the replies section
            repliesSection.appendChild(replyField);
        }

        toggleDeleteButton(sender, messageId);

        // Display existing replies
        if (message.replies && message.replies.length > 0) {

            var repliesList = document.createElement('ul');
            repliesList.className = 'list-unstyled';
            message.replies.forEach(function (reply) {
                console.log('Reply', reply);
                const created_date = new Date(reply.created);

                const formattedDate = `${created_date.toDateString()} ${created_date.toLocaleTimeString()} (EAT)`;

                var replyItem = document.createElement('li');
                repliesSection.className = 'me-3';
                replyItem.innerHTML = `
                <div id="reply-${reply.id}" data-created="${created}">
                    <span style="margin-left: 30px;">
                        <i class="fas fa-comments text-success"></i>
                        <span style="font-weight: bold; margin-left: 0.5rem;">${reply.sender}: </span>
                        <span style="color: #975344; margin-left: 0.5rem;">replied...</span>
                        <span style="color: green;">${reply.content}</span>
                        - sent on ${formattedDate}
                        <button class="btn btn-sm ms-2"  onclick="deleteReply(${messageId}, ${reply.id})" id="deleteReplyButton-${messageId}-${reply.id}" style="color: #975344;">
                        <i class="material-icons small">delete</i>
                        </button>
                    </span>
                </div>
                `;

                repliesList.appendChild(replyItem);
                // Call toggleDeleteReplyButton to handle button visibility
                toggleDeleteReplyButton(reply.sender, messageId, reply.id);
            });
            repliesSection.appendChild(repliesList);
        }

        // Sort the chat container based on created dates (latest first)
        sortChatContainer();

    } else {
        // Create a new message element
        var messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.id = 'message-' + messageId;
        messageElement.innerHTML = `
        <div id="message-${messageId}" data-created="${created}">
         <div class="d-flex align-items-center">
            <img src="${senderPhotoUrl || '/media/profile_photos/blank-avatar.png'}" alt="Profile Photo" class="rounded-circle overflow-hidden me-2" style="width: 35px; height: 35px;" onerror="this.onerror=null; this.src='/media/profile_photos/avatar-user.svg';">
            <span style="font-weight: bold;">${sender}:</span>
            <span style="color: #975344; margin-left: 0.5rem;">shared...</span>
           </div>
            <span style="color: green; margin-left: 0.5rem;">${content}</span>
            - sent on ${formattedDate}
            <button class="btn btn-sm ms-2" onclick="toggleReplyField('${sender}', ${messageId})" style="color: green;">
                <i class="material-icons small">reply</i>
            </button>
            <button class="btn btn-sm ms-2" onclick="deleteMessage('${sender}', ${messageId})" id="deleteButton-${messageId}" style="color: #975344;">
                <i class="material-icons small">delete</i>
            </button>
        </div>
        <hr>
        `;

        // Prepend the message to the chat container
        document.getElementById('chat-container').prepend(messageElement);

         // Call the toggleDeleteButton function to handle the visibility of the delete button
        toggleDeleteButton(sender, messageId);

        var replyField = document.createElement('textarea');
        replyField.className = 'form-control mt-2 d-none';
        replyField.placeholder = 'Reply to ' + sender + '...';
        replyField.id = 'replyField-' + messageId;
        messageElement.appendChild(replyField);

        var repliesSection = document.createElement('div');
        repliesSection.className = 'replies-section mt-2 d-none';
        repliesSection.id = 'repliesSection-' + messageId;
        messageElement.appendChild(repliesSection);

        // Display existing replies
        if (message.replies && message.replies.length > 0) {
            var repliesList = document.createElement('ul');
            repliesList.className = 'list-unstyled';
            message.replies.forEach(function (reply) {
                var replyItem = document.createElement('li');
                repliesSection.className = 'me-3';
                replyItem.innerHTML = `
                <span style="margin-left: 30px;">
                    <i class="fas fa-comments text-success"></i>
                    <span style="font-weight: bold; margin-left: 0.5rem;">${reply.sender}: </span>
                    <span style="color: #975344; margin-left: 0.5rem;">replied...</span>
                    <span style="color: green;">${reply.content}</span>
                    - sent on ${formattedDate}
                </span>
            `;
                repliesList.appendChild(replyItem);
            });
            repliesSection.appendChild(repliesList);
        }

        // Store the latest message for the user
        latestMessages[sender] = messageElement;
    }
}

// Function to sort the chat container based on created dates (latest first)
function sortChatContainer() {
    var chatContainer = document.getElementById('chat-container');
    var messages = Array.from(chatContainer.getElementsByClassName('message'));

    messages.sort(function (a, b) {
        var dateA = a.querySelector('[data-created]') ? new Date(a.querySelector('[data-created]').getAttribute('data-created').replace(/-/g, '/')) : 0;
        var dateB = b.querySelector('[data-created]') ? new Date(b.querySelector('[data-created]').getAttribute('data-created').replace(/-/g, '/')) : 0;

        // If data-created attribute is not defined, skip the element in the sorting
        if (dateA === 0 || dateB === 0) {
            return 0;
        }

        return dateB - dateA;
    });

    // Clear the chat container
    chatContainer.innerHTML = '';

    // Append sorted messages to the chat container
    messages.forEach(function (message) {
        chatContainer.appendChild(message);
    });
}

// handles sending of new messages
function sendMessage() {
    // Get the message content from the input field
    var messageContent = document.getElementById('messageContent').value;

    if (!messageContent.trim()) {
        // If content is empty or contains only whitespace, don't send the message
        return;
    }

    // Send the message via AJAX
    fetch('/windwood/chatroom/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: 'content=' + encodeURIComponent(messageContent),
    })
    .then(response => response.json())
    .then(data => {
        // Update the chat container with the latest message and messageId
        updateChatContainer(data.message, data.messageId);
        //clear the message field
        document.getElementById('messageContent').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

//fetches existing messages and notifies the webscoket
async function fetchLatestMessagesAndNotifyWebSocket(socket) {
    try {
        const response = await fetch(fetchMessagesUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        if (data.success) {

            const messages = data.messages;

            // Use a for...of loop to ensure asynchronous processing in order
            for (const message of messages) {
                // Update the chat container with the latest message
                updateChatContainer(message);

                // Check if the message ID has been processed on the server side
                const isProcessedOnServer = await checkIfMessageIsProcessedOnServer(message.id);

                // Check if the message ID has been processed locally
                if (!isProcessedOnServer) {
                    console.log('Received WebSocket message..:', message);

                    // Notify the WebSocket with the new message
                    notifyWebSocket(message, socket);

                }
            }

            // Store the latest messages in local storage
            localStorage.setItem('latestMessages', JSON.stringify(messages));

        } else {
            // Handle failure if needed
            console.error('Failed to fetch existing messages:', data.error);
        }
    } catch (error) {
        console.error('Error fetching existing messages:', error);
        // Handle error if needed
    }
}

// Function to check if a message is processed on the server
async function checkIfMessageIsProcessedOnServer(messageId) {

    try {
        const response = await fetch(checkIfMessageProcessedUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ messageId }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data.isProcessed || false;
    } catch (error) {
        console.error('Error checking if message is processed on the server:', error);
        return false;
    }
}

// Function to mark a message as processed on the server
async function markMessageAsProcessedOnServer(messageId) {

    try {
        const response = await fetch(markMessageAsProcessedUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ messageId }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

    } catch (error) {
        console.error('Error marking message as processed on the server:', error);
        // Handle error if needed
    }
}

function notifyWebSocket(message, socket) {
   
    // Add the 'type' field to the message
    message.type = 'chat.notification';

    // Notify the WebSocket with the new message
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    } else {
        console.error("WebSocket connection not in OPEN state. Cannot notify WebSocket.");
    }
}

// WebSocket Connections
document.addEventListener("DOMContentLoaded", function () {
    var wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    var wsPath = wsProtocol + "://" + window.location.host + "/ws/chat/";
    var socket = new WebSocket(wsPath);

    // Variable to store accumulated messages
    let messages = [];

    socket.onopen = function (event) {
        console.log("WebSocket connection opened:", event);
    
        if (socket.readyState === WebSocket.OPEN) {
            // Call the initializeChat function when the WebSocket connection is open
            initializeChat();
        } else {
            console.error("WebSocket connection not in OPEN state.");
        }
    };

    
    socket.onmessage = async function (event) {
        try {
            var data = JSON.parse(event.data);
    
            // Push the received message into the messages array
            messages.push(data);

            // Check the type of message and take appropriate action
            if (data.type === 'chat.notification') {
                // Display the notification in the chat UI
    
                // Call displayNotification with a callback and a copy of the messages array
                displayNotification([...messages], async (userClickedOK, messageIds) => {
                    if (userClickedOK && messageIds) {
                        // Mark the messages as processed on the server
                        await handleNotificationInteraction(userClickedOK, messageIds);
                    } else {
                        console.log('User canceled or did not confirm');
                        // Handle the case where the user canceled or did not confirm viewing the notification
                    }
    
                    // Clear the messages array after displaying notifications
                    messages = [];
                });
            } else {
                // update the chat UI for regular messages
                updateChatContainer(data);
            }
        } catch (error) {
            console.error("Error handling WebSocket message:", error);
        }
    };
    

    socket.onclose = function (event) {
        console.log("WebSocket connection closed:", event);
    };

    // Function to initialize the chat
   
    async function initializeChat() {
        try {
            const currentUserData = await getCurrentUser();

            if (currentUserData) {
                // Load messages from local storage if available
                const storedMessages = localStorage.getItem('latestMessages');
                if (storedMessages) {
                    messages = JSON.parse(storedMessages);
                    // Update the chat UI with stored messages
                    messages.forEach(message => updateChatContainer(message));
                }

                await fetchLatestMessagesAndNotifyWebSocket(socket);
            } else {
                throw new Error('Current user data not available.');
            }
        } catch (error) {
            console.error('Error initializing chat:', error);
        }
    }
});

