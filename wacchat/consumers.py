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
    async def disconnect(self):
        # Your disconnect logic here
        pass
    async def receive(self, text_data):
        # Send the current time every 3 seconds, 5 times
        # for i in range(5):
        #         response = countNumer(i,text_data) 
        #         current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #         await self.send(text_data=current_time + "---" + str(response))
        #         await asyncio.sleep(1) 
        try:
            # Convert the received text_data to an integer
            iterations = int(text_data)
            if iterations <= 0:
                await self.send(text_data="Invalid number of iterations.")
                await self.disconnect()
                return
        except ValueError:
                await self.send(text_data="Invalid input. Please provide a valid number.")
                await self.disconnect()
                return
        
        for i in range(1, iterations + 1):
                # Send the current progress as a fraction (e.g., 1/10, 2/10)
                print(i)
                await self.send(text_data=f"Progress: {i}/{iterations}")
                # Wait for 3 seconds before sending the next progress update
                await asyncio.sleep(3)

        
        # Send an end message
        await self.send(text_data="Process finished.")
        self.disconnect()
