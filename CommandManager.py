import re
import asyncio
import Commands


argument_regex = re.compile(r'(\S+)|(".*")')
text_channel_regex = re.compile(r'<#\d+>')
member_notify_regex = re.compile(r'<@\d+>')


system_commands = {
    "play": {
        "description": "Plays the video's audio at the specified URL.",
        "num-args": 1
    },
    "stop": {
        "description": "Stops all audio output.",
        "num-args": 0
    }
}


class CommandManager:
    def __init__(self, client, config, commands, sfx_manager):
        self.client = client
        self.config = config
        self.sfx_commands = commands
        self.sfx_manager = sfx_manager

    @asyncio.coroutine
    def process(self, message):
        message_string = message.content

        for command in self.sfx_commands:
            prefix = self.sfx_commands[command].get('prefix')
            if not prefix:
                prefix = self.config.get('default-sfx-command-prefix', '')

            if not message.content.lower().startswith(prefix + command):
                continue

            self.sfx_manager.play(self.sfx_commands[command]['filename'], message.channel, message.author.voice_channel,
                                  message.author)
            return

        result = re.search(member_notify_regex, message_string)
        if not result:
            return
        result = result.group(0)
        if self.config['bot-id'] not in result:
            return
        message_string = re.sub(member_notify_regex, '', message_string).strip()

        for command in system_commands:
            if not message_string.startswith(command):
                continue

            message_string = message_string.replace(command, '', 1)

            arg_string = message_string.replace(command, '')
            num_args = system_commands[command]['num-args']
            args = [x.group(0) for x in re.finditer(argument_regex, arg_string)]

            if len(args) != num_args:
                yield from self.client.send_message(message.channel,
                                                    "Incorrect arguments for the specified command.")
                return

            if hasattr(Commands, command):
                reply = yield from getattr(Commands, command)(self, message.author, message.channel, args)
                if reply:
                    yield from self.client.send_message(message.channel, reply)
                    return
