import asyncio


class SFXManager:
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.running = False
        self.player = None
        self.queue = []

    def play(self, filepath, text_channel, voice_channel, caller):
        self.queue.append([filepath, text_channel, voice_channel, caller])

    @asyncio.coroutine
    def process(self):
        while True:
            yield from asyncio.sleep(0.5)
            if self.running:
                continue
            if self.queue:
                filepath, text_channel, voice_channel, caller = self.queue.pop(0)
                voice = self.client.voice
                if self.client.is_voice_connected():
                    if voice_channel != self.client.voice.channel:
                        self.client.voice.disconnect()
                        voice = yield from self.client.join_voice_channel(voice_channel)
                else:
                    voice = yield from self.client.join_voice_channel(voice_channel)

                filepath = self.config.get('sfx-path', 'sfx/') + filepath
                self.player = voice.create_ffmpeg_player(filepath, after=self.cont)
                self.running = True
                self.player.start()
            elif self.client.voice:
                self.client.voice.disconnect()

    def cont(self):
        self.player = None
        self.running = False
