import random


class MessageManager:

    def __init__(self, message):
        self.message = message
        self.messages = []

    def get_status(self):
        self.messages = [
            {
                'name': '$Devices',
                'message': 'Devices online: {}'.format(random.randint(0, 20))
            },
            {
                'name': '$Allowed',
                'message': 'Devices Allowed online: {}'.format(random.randint(0, 20))
            },
        ]

    def get_message(self):
        self.get_status()
        for message in self.messages:
            if message['name'] == self.message:
                return message['message']
        return 'Test'
