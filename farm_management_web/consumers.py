import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime, timedelta

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accumulated_messages = {}

    async def connect(self):
        print("WebSocket connected")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("Received WebSocket message:", text_data)
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == 'chat.notification':
                await self.handle_notification(text_data_json)
            else:
                # Handle other types of messages as needed
                pass

        except json.JSONDecodeError as e:
            print('Failed to decode JSON:', e)

    async def handle_notification(self, message):
        sender_name = message['sender']
        message_id = message['id']

        # Check if there are accumulated messages for this sender
        if sender_name not in self.accumulated_messages:
            self.accumulated_messages[sender_name] = []

        # Add the new message to the accumulated messages list
        self.accumulated_messages[sender_name].append(message_id)

        # Log the received message to the console
        print(f"Received notification from {sender_name}: {message['content']}")

        # Check if it's time to send a consolidated notification
        if len(self.accumulated_messages[sender_name]) > 1: 
            await self.send_consolidated_notification(sender_name)

    async def send_consolidated_notification(self, sender_name):
        # Get the accumulated messages for this sender
        accumulated_message_ids = self.accumulated_messages[sender_name]

        # Clear the accumulated messages for this sender
        self.accumulated_messages[sender_name] = []

        # Log the consolidated notification to the console
        print(f"Sending consolidated notification to {sender_name}: {len(accumulated_message_ids)} new messages")

        # Send the consolidated notification to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat.notification',
            'sender': sender_name,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'content': f"You have {len(accumulated_message_ids)} new messages. Check the chat!",
            'id': accumulated_message_ids  # Send the list of accumulated message IDs for processing
        }))
