import numpy as np
import pyaudio

from adapters.midi import MidiDriver
from adapters.midi_message import MidiMessage
from adapters.reader import AudioReader
from core.phrase import Phrase
from core.states import State
from core.states.expression import ExpressionState
from core.states.play import PlayState
from core.states.record import RecordState
from core.states.stop import StopState


class Session(object):
    def __init__(self, midi_out, midi_in):
        # Midi setup
        self.timestamp = 0
        self.midi = MidiDriver(midi_out, midi_in)
        self.midi.midi_in.set_callback(self.on_midi)

        # Audio setup
        phrase_ids = list(range(1, 5))
        self.wave_reader = AudioReader(self.callback, phrase_ids)

        # Controller setup
        args = [self.wave_reader.channels, self.wave_reader.frames_per_buffer]
        self.phrases = dict([(i, Phrase(i, *args)) for i in phrase_ids])
        # todo : session object mustve acccess to only active state rest all must be crete by looper
        self.active_phrase = self.phrases[self.midi.active_phrase]

        # State of the looper setup
        self.states = {State.STOP: StopState(self), State.RECORD: RecordState(self), State.PLAY: PlayState(self),
                       State.EXPRESSION: ExpressionState(self)}
        self.active_state = self.states[State.STOP]

    def callback(self, in_data, frame_count, time_info, status):
        output_arr = np.fromstring(in_data, dtype=np.int16)
        output_arr = self.active_state.on_state(output_arr, self.active_phrase)
        return output_arr.astype(np.int16), pyaudio.paContinue

    def on_midi(self, message, data):
        midi = MidiMessage(message)
        try:
            phrase_id, state_id = self.active_state.actions[midi.function](midi, self.active_phrase)
        except Exception as err:
            print(err)
        # self.active_phrase = self.phrases[phrase_id]
        # self.active_state = self.states[state_id]
        # if state_id == State.EXPRESSION:
        #     self.write_phrases()

    def write_phrases(self):
        for i, phrase in self.phrases.items():
            if len(phrase.layers) == 0:
                pass
            for layer in phrase.layers:
                self.wave_reader.write_layer(i, layer)
