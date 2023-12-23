import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
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
                await self.send_notification({'message': text_data_json})
            else:
                # Handle other types of messages as needed
                pass

        except json.JSONDecodeError as e:
            print('Failed to decode JSON:', e)

    async def send_notification(self, message):
        
        # Handle chat.notification events sent by the server
        message_content = message['message']['content']
        sender_name = message['message']['sender']
        created_date = message['message']['created']

        # Log the received message to the console
        print(f"Received notification from {sender_name} at {created_date}: {message_content}")

        # Send the notification to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat.notification',
            'sender': sender_name,
            'created': created_date,
            'content': message_content,
        }))


