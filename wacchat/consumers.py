import asyncio
import datetime
import json
import os
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer
from wacchat.ia import countNumer
class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Send the current time every 3 seconds, 5 times
        for i in range(5):
                response = countNumer(i,text_data)  # Assuming countNumer is a function that returns the message
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await self.send(text_data=current_time + "---" + str(response))
                await asyncio.sleep(1)  # Adjust the sleep time as needed
        # Send an end message
        await self.send(text_data="Process finished.")
        self.disconnect()
