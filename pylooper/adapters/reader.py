import os
import uuid
import wave

import pyaudio


class AudioReader(object):
    def __init__(self, callback, phrase_ids, base="../VLoop/"):
        self.session_id = str(uuid.uuid4())
        self.folder = base + self.session_id
        for phrase_id in phrase_ids:
            os.makedirs("%s/phrase_%s" % (self.folder, str(phrase_id)))
        self.frames_per_buffer = 256
        self.sample_rate = 44100
        self.channels = 1
        self.width = 2  # must change with the audio format ,  2 *bytes =16 format
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=self.channels, output=True,
                                             rate=self.sample_rate, input=True,
                                             frames_per_buffer=self.frames_per_buffer, stream_callback=callback)

    def write_layer(self, i, layer):
        file_hash = str(hash(str(layer.data[0])))
        file_name = "%s/phrase_%s/%s.wav" % (self.folder, str(i), file_hash)
        if not os.path.exists(file_name):
            with wave.open(file_name, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.width)
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(layer.data))

