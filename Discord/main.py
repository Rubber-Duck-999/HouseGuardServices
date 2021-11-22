import discord
import json
from message import MessageManager
import logging
from discord.ext import tasks
import os

try:
	os.remove('/home/pi/Documents/HouseGuardServices/discord.log')
except:
	print("The log did not exist")

logging.basicConfig(filename='/home/pi/Documents/HouseGuardServices/discord.log',
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

class HouseClient(discord.Client):

    def __init__(self, *args, **kwargs):
        '''Sub constructor'''
        self.guild = ''
        super().__init__(*args, **kwargs)
        self.channel = 'general'

    def get_settings(self):
        '''Get config env var'''
        logging.info('get_settings()')
        config_name = '/home/pi/Documents/HouseGuardServices/config.json'
        token = ''
        try:
            with open(config_name) as file:
                data = json.load(file)
            self.guild = data["guild"]
            token = data["token"]
            self.message_manager = MessageManager()
            self.message_manager.get_env()
            self.message_manager.get_status()
        except KeyError:
            logging.error("Variables not set")
        except IOError:
            logging.error('Could not read file')
        return token

    @tasks.loop(minutes = 30)
    async def task(self):
        logging.info("task()")
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.name == 'general':
                    await channel.send('Checking service status')

    async def on_ready(self):
        self.task.start()
        for guild in client.guilds:
            if guild.name == self.guild:
                logging.debug('Same guild on join')
                self.guild = guild
                break

        logging.info('{} is connected to the following guild: {}'.format(client.user, self.guild))

        for guild in client.guilds:
            for channel in guild.channels:
                if channel.name == 'general':
                    await channel.send('Starting Server')

    async def on_message(self, message):
        if message.author == client.user:
            return

        sentence = self.message_manager.get_message(message.content)

        await message.channel.send(sentence)


if __name__ == "__main__":
    logging.info('Starting Program')
    client = HouseClient()
    token = client.get_settings()
    if len(token) > 1:
        client.run(token)