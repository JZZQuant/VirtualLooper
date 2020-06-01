import pyaudio


class AudioReader(object):
    def __init__(self, callback):
        self.frames_per_buffer = 256
        self.sample_rate = 44100
        self.channels = 2
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=self.channels, output=True,
                                             rate=self.sample_rate, input=True,
                                             frames_per_buffer=self.frames_per_buffer, stream_callback=callback)
