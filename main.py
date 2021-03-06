import json
import discord
import asyncio


from CommandManager import CommandManager
from SFXManager import SFXManager
import Util

config = Util.get_config()
sfx_commands = Util.get_commands()

discord.opus.load_opus(config.get('opus-path', 'libopus/libopus-0.dll'))

client = discord.Client()
sfx_manager = SFXManager(client, config)
command_manager = CommandManager(client, config, sfx_commands, sfx_manager)


@asyncio.coroutine
def main():
    yield from client.login(config.get('client-token'))
    yield from client.connect()


@client.event
async def on_ready():
    print('You are now logged in!')
    print('Username:' + client.user.name)


@client.async_event
async def on_message(message):
    await command_manager.process(message)


loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(sfx_manager.process())
    loop.run_until_complete(main())
except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
