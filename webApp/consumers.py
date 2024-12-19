import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
     
    async def connect(self):
        print("connect  to add order group")
        await self.channel_layer.group_add("notifications_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications_group", self.channel_name)

    async def receive(self, text_data):
        pass  # We're not expecting to receive any messages from the client

    async def send_order_notification(self, event):
        print("was sent web socket mesej")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))


class OrderListingConsumer(AsyncWebsocketConsumer):
     
    async def connect(self):
        print("connect  to orders listing group")
        await self.channel_layer.group_add("orders_listing_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders_listing_group", self.channel_name)

    async def receive(self, text_data):
        pass  # We're not expecting to receive any messages from the client

    async def send_order_list_notification(self, event):
        print("in order list web socket mesej")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))
