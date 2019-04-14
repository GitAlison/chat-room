import asyncio
import json
from datetime import datetime

from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread,ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("Connected",event)
        await self.send({
            'type':'websocket.accept'
        })
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me,other_user)
        chat_room  = f"thread_{thread_obj.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name 
        )

        print(me,thread_obj.id)


        

    async def websocket_receive(self, event):
        print("Receive", event)
        front_text = event.get('text',None)
        if front_text is not None:
            dict_data = json.loads(front_text)
            msg = dict_data.get('message')
            print(msg)
            
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                'message' : msg,
                'username' : username
            }

            new_event = {
                "type":"websocket_send",
                "text":json.dumps(myResponse)
            }
            await self.channel_layer.group_send(
                self.chat_room,
                { 
                    "type":"chat_message",
                    "text":json.dumps(myResponse)
                }
            )
            

    async def chat_message(self,event):
        print('message',event)
        await self.send({
            "type":"websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("Disconect", event)

    @database_sync_to_async
    def get_thread(self,user,other_user):
        return Thread.objects.get_or_new(user,other_user)[0]