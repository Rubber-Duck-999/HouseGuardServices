#!/usr/bin/python3
'''Discord script'''
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
        self.message_channel = 'general'
        self.authors = []

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
            self.authors = data["authors"]
            self.message_manager = MessageManager()
            self.message_manager.get_env()
            self.message_manager.get_status()
        except KeyError:
            logging.error("Variables not set")
        except IOError:
            logging.error('Could not read file')
        return token

    def check_author(self, sender):
        '''Check message author'''
        logging.info('check_author()')
        logging.info(sender)
        for author in self.authors:
            logging.info(author)
            if author == sender:
                return True
        return False

    @tasks.loop(minutes=60)
    async def task(self):
        logging.info("task()")
        status = self.message_manager.get_status()
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.name == 'status':
                    await channel.send('Checking service status: {}'.format(status))

    async def on_ready(self):
        self.task.start()
        for guild in client.guilds:
            if guild.name == self.guild:
                logging.debug('Same guild on join')
                self.guild = guild
                break

        logging.info('{} is connected to the following guild: {}'.format(
            client.user, self.guild))

        for guild in client.guilds:
            for channel in guild.channels:
                if channel.name == 'status':
                    await channel.send('Starting Server')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.channel == self.message_channel:
            logging.info('Wrong channel: {}'.format(message.channel))
            return

        if self.check_author(message.author):
            await message.channel.send('### Beep - Calculating ###')
            responses = self.message_manager.get_message(message.content)
            for response in responses:
                await message.channel.send(response)
        else:
            logging.error(
                'Someone unexpected talked to us, run!: {}'.format(message.author))


if __name__ == "__main__":
    logging.info('Starting Program')
    client = HouseClient()
    token = client.get_settings()
    if len(token) > 1:
        client.run(token)
