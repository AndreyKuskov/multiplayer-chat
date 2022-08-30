import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from . import models

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        insert = models.ActiveUsers.objects.get_or_create(user=self.user, chat=models.Chat.objects.get(name=self.room_name))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'users_list',
                'message': f'{self.user} has joined the chat'
            }
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        user = models.ActiveUsers.objects.get(user=self.user, chat=models.Chat.objects.get(name=self.room_name))
        user.delete()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'users_list',
                'message': f'{self.user} has left the chat'
            }
        )

    def users_list(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'hello': message, 
            'users': json.dumps(list(models.ActiveUsers.objects.filter(chat__name=self.room_name).distinct('user', 'chat').values("user__username")), cls=DjangoJSONEncoder),
        }))

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        insert = models.Messages.objects.create(message=message, user=self.user, chat=models.Chat.objects.get(name=self.room_name))
        insert.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))