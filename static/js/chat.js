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
                    replyItemElement.innerHTML = '<span style="font-weight: bold;">' + replyItem.sender + ':</span> ' + replyItem.content;
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
        console.log('Message removed successfully.');
    } else {
        console.error('Message element not found for messageId:', messageId);
    }
}

// If Message gas Replies Remove replies from the UI
function removeReply(message_id) {
    // Implement the logic to remove the reply section from the UI
    var repliesSection = document.getElementById('repliesSection-' + message_id);

    if (repliesSection) {
        repliesSection.remove();
    } else {
        console.error('Replies section not found:', 'repliesSection-' + message_id);
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
                // Remove the deleted message and its replies from the UI
                removeMessage(sender, messageId);

                if (data.message_id) {
                    removeReply(data.message_id);
                }

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

// Function to display a simple notification
async function displayNotification(message) {
    try {
        const currentUserData = await getCurrentUser();
 
        // Ensure currentUserData is resolved before proceeding
        if (currentUserData && message.sender !== currentUserData.username) {
            // Display the notification
            alert(`New Message Posted By ${message.sender}\nMessage: ${message.content}\nCheck the Chat!`);
        } else {
            console.log('Skipping notification for own message:', message);
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

                const created_date = new Date(reply.created);

                const formattedDate = `${created_date.toDateString()} ${created_date.toLocaleTimeString()} (EAT)`;

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

// Retrieve processedMessageIds from local storage or initialize an empty set
const processedMessageIds = new Set(JSON.parse(localStorage.getItem('processedMessageIds')) || []);

async function fetchExistingMessagesAndNotifyWebSocket(socket) {
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

            // Append each existing message to the chat container
            data.messages.forEach(function (message) {
                // Update the chat container with the latest message
                updateChatContainer(message);

                // Check if the message ID has been processed
                if (!processedMessageIds.has(message.id)) {
                    // Notify the WebSocket with the new message
                    notifyWebSocket(message, socket);

                    // Add the message ID to the processed set
                    processedMessageIds.add(message.id);
                }
            });
            // Save the updated processedMessageIds to local storage
            localStorage.setItem('processedMessageIds', JSON.stringify(Array.from(processedMessageIds)));
        } else {
            // Handle failure if needed
            console.error('Failed to fetch existing messages:', data.error);
        }
    } catch (error) {
        console.error('Error fetching existing messages:', error);
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

    socket.onopen = function (event) {
        console.log("WebSocket connection opened:", event);
    
        if (socket.readyState === WebSocket.OPEN) {
            // Call the initializeChat function when the WebSocket connection is open
            initializeChat();
        } else {
            console.error("WebSocket connection not in OPEN state.");
        }
    };

    socket.onmessage = function (event) {
        try {
            var data = JSON.parse(event.data);
            var message = data;

            // Check the type of message and take appropriate action
            if (message.type === 'chat.notification') {
                // Display the notification in the chat UI
                displayNotification(message);
            } else {
                // update the chat UI for regular messages
                updateChatContainer(message);
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
            // Fetch the current user data first
            const currentUserData = await getCurrentUser();

            // If the current user data is available
            if (currentUserData) {
                // Fetch and display existing messages
                await fetchExistingMessagesAndNotifyWebSocket(socket);
            } else {
                console.error('Current user data not available.');
                // Handle the case where current user data is not available
            }
        } catch (error) {
            console.error('Error initializing chat:', error);
            // Handle error if needed
        }
    }
});

