from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.models import User
from.models import Thread, Chatroom, get_or_create_personal_thread
from channels.consumer import SyncConsumer

class chatroom(WebsocketConsumer):
    def connect(self):
            other_username=self.scope['url_route']['kwargs']['username']
            user=User.objects.get(username=other_username)
            superuser = User.objects.get(is_superuser=True)
            thread_obj=get_or_create_personal_thread(superuser, user)
            self.roomname = f'personal_thread_{thread_obj}'
            print(self.roomname)
            async_to_sync(self.channel_layer.group_add)(
                self.roomname,
                self.channel_name
                )
            print(f'[{self.channel_name}] - you are connected')
            self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.roomname,
            self.channel_name
        )

    def receive(self, text_data):
        print(f'[{self.channel_name}] - Receive message- {text_data}')
        async_to_sync(self.channel_layer.group_send)(
            self.roomname, {
                'type':'chat_message',
                'message': text_data,
            }
        )

    def chat_message(self, event):
        message = event['message']
        data = json.loads(message)
        self.send(text_data=json.dumps({
            'message': data['message']
        }))