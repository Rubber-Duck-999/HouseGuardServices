import discord
import json
from message import MessageManager


class HouseClient(discord.Client):

    def __init__(self, *args, **kwargs):
        '''Sub constructor'''
        self.guild = ''
        super().__init__(*args, **kwargs)

    def get_settings(self):
        '''Get config env var'''
        print('get_settings()')
        config_name = '/home/simon/Documents/HouseGuardServices/config.json'
        token = ''
        try:
            with open(config_name) as file:
                data = json.load(file)
            self.guild = data["guild"]
            token = data["token"]
        except KeyError:
            print("Variables not set")
        except IOError:
            print('Could not read file')
        return token

    async def on_ready(self):
        for guild in client.guilds:
            if guild.name == self.guild:
                print('Same guild')
                self.guild = guild
                break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{self.guild.name}(id: {self.guild.id})'
        )

        general = None
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.name == 'general':
                    general = channel
                    await general.send('$Starting Server')

    async def on_message(self, message):
        if message.author == client.user:
            return

        message_manager = MessageManager(message.content)

        sentence = message_manager.get_message()

        await message.channel.send(sentence)


client = HouseClient()
token = client.get_settings()

client.run(token)
