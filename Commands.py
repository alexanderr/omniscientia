import re
from youtube_dl.utils import DownloadError

youtube_regex = re.compile(r'(youtube\.com/watch\?v=\S+)|(youtu\.be/\S+)')

youtube_player = None


def play(mgr, user, channel, args):
    global youtube_player
    client = mgr.client
    url = re.search(youtube_regex, args[0])
    if not url:
        return "Invalid URL specified."
    url = url.group(0)

    voice = client.voice
    if client.is_voice_connected():
        if user.voice_channel != client.voice.channel:
            yield from client.voice.disconnect()
            voice = yield from client.join_voice_channel(user.voice_channel)
    else:
        voice = yield from client.join_voice_channel(user.voice_channel)

    if youtube_player is not None and youtube_player.is_done():
        yield from youtube_player.stop()

    mgr.sfx_manager.queue = []

    if mgr.sfx_manager.running:
        yield from mgr.sfx_manager.player.stop()
        mgr.sfx_manager.running = False

    try:
        youtube_player = yield from voice.create_ytdl_player(url=url)
    except DownloadError:
        return "That video does not exist!"

    youtube_player.start()
    return "Playing: " + youtube_player.title


def stop(mgr, user, channel, args):
    if youtube_player is not None:
        youtube_player.stop()

    if mgr.sfx_manager.player is not None:
        mgr.sfx_manager.player.stop()
