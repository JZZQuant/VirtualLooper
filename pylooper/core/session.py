import numpy as np
import pyaudio

from adapters.midi_message import MidiMessage
from adapters.reader import AudioReader
from core.phrase import Phrase
from core.states.expression import ExpressionState
from core.states.play import PlayState
from core.states.record import RecordState
from core.states.stop import StopState


class Session(object):
    def __init__(self, midi):
        self.midi = midi
        phrase_ids = list(range(1, 5))
        self.wave_reader = AudioReader(self.callback, phrase_ids)
        c = self.wave_reader.channels
        f = self.wave_reader.frames_per_buffer
        s = self.wave_reader.sample_rate

        self.phrases = dict(
            zip(phrase_ids, [Phrase(c, f, s, id) for id in phrase_ids]))
        self.active_phrase = self.phrases[self.midi.active_phrase]
        self.timestamp = 0
        self.stop = StopState(self)
        self.record = RecordState(self)
        self.play = PlayState(self)
        self.switch = ExpressionState(self)
        self.active_state = self.stop

    def callback(self, in_data, frame_count, time_info, status):
        output_arr = np.fromstring(in_data, dtype=np.int16)
        output_arr = self.active_state.on_state(output_arr, self.active_phrase)
        return output_arr.astype(np.int16), pyaudio.paContinue

    def on_midi(self, message, data):
        midi = MidiMessage(message)
        self.active_state.actions[midi.function](midi, self.active_phrase)

    def write_phrases(self):
        for i, phrase in self.phrases.items():
            if len(phrase.layers) == 0:
                pass
            else:
                for layer in phrase.layers:
                    self.wave_reader.write_layer(i, layer)

    def reset_session(self):
        self.write_phrases()
        temp = self.midi
        self.__init__(temp)
        self.midi.send1()
