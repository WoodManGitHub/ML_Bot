import discord
import numpy as np
import urllib.request
from queue_util import RAISRQueue
import re

queue = RAISRQueue()


class RAISR_BOT(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="RAISR"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if str(message.channel.type) == 'private':
            if message.attachments:
                await message.channel.send(
                    'Please wait... Your picture has been added to the queue.')
                url = message.attachments[0].url
                file_Name = re.match(
                    r'https:\/\/cdn\.discordapp\.com\/attachments\/.*\/(.*)', url).group(1)
                req = urllib.request.Request(
                    url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                await queue.queue_and_upscaple(file_Name, image, message)


client = RAISR_BOT()
client.run('Token')
