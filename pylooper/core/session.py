import numpy as np
import pyaudio

from adapters.midi import MidiDriver
from adapters.reader import AudioReader
from core.phrase import Phrase
from core.states.expression import ExpressionState
from core.states.play import PlayState
from core.states.record import RecordState
from core.states.stop import StopState


class Session(object):
    def __init__(self, midi_out, midi_in):
        self.auto_start_threshold = []
        # todo : session object mustve acccess to only active phrase rest all must be crete by looper
        self.midi = MidiDriver(midi_out, midi_in)
        self.midi.midi_in.set_callback(self.on_midi)
        self.phrase_ids = list(range(1, 5))
        self.wave_reader = AudioReader(self.callback, self.phrase_ids)
        self.phrases = dict(
            zip(self.phrase_ids, [Phrase(self.wave_reader.channels, self.wave_reader.frames_per_buffer)] * 4))
        # todo : session object mustve acccess to only active state rest all must be crete by looper
        self.active_phrase = self.phrases[self.midi.active_phrase]
        self.timestamp = 0
        self.states = {"Stop": StopState(self), "Record": RecordState(self), "Play": PlayState(self),
                       "Rhythm": ExpressionState(self)}
        self.active_state = self.states["Stop"]
        self.control_on = False
        self.expression_on = False
        self.exp_on = False
        self.switch_on = False
        self.back_vol = 1
        self.program_on = False

    def callback(self, in_data, frame_count, time_info, status):
        array_input_fromstring = np.fromstring(in_data, dtype=np.int16)
        processed_signal_for_output, new_state = self.active_state.on_state(array_input_fromstring, self.active_phrase,
                                                                            self.back_vol)
        self.active_state = self.states[new_state]
        return processed_signal_for_output.astype(np.int16), pyaudio.paContinue

    def on_midi(self, message, data):
        midi = message[0]
        self.timestamp += message[1]
        # todo :modify these to logger info messages
        print("received message :%s at time %f" % (midi, self.timestamp))
        # todo : create a midi datastrcuture and push the 'if' to that class
        if midi[0] == 192:
            new_state = self.active_state.on_program_change(midi[1], active_phrase=self.active_phrase,
                                                            time_delta=message[1], midi=midi)
        else:
            new_state = self.active_state.actions[midi[1]](midi[2], active_phrase=self.active_phrase,
                                                           time_delta=message[1], midi=midi)
        self.active_state = self.states[new_state]

    def write_phrases(self):
        for i, phrase in self.phrases.items():
            if len(phrase.layers) == 0:
                pass
            for layer in phrase.layers:
                self.wave_reader.write_layer(i, layer)
