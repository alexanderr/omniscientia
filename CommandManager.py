
class CommandManager:
    def __init__(self, client, config, commands, sfx_manager):
        self.client = client
        self.config = config
        self.commands = commands
        self.sfx_manager = sfx_manager

    def process(self, message):
        for command in self.commands:
            if message.content.lower() != command:
                continue

            if self.commands[command]['type'] == 'sfx':
                self.sfx_manager.play(self.commands[command]['filename'], message.channel, message.author.voice_channel,
                                      message.author)
                return
