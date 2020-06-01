import numpy as np
import pyaudio

from core.adapters.midi import MidiDriver
from core.adapters.reader import AudioReader
from core.adapters.writer import AudioWriter
from core.phrase import Phrase
from core.states.expression import ExpressionState
from core.states.play import PlayState
from core.states.record import RecordState
from core.states.stop import StopState


class Session(object):
    def __init__(self, midi_out, midi_in):
        self.auto_start_threshold = []
        self.midi = MidiDriver(midi_out, midi_in)
        self.phrases = {1: Phrase(), 2: Phrase(), 3: Phrase(), 4: Phrase()}
        self.active_phrase = self.phrases[self.midi.active_phrase]
        self.midi.midi_in.set_callback(self.on_midi)
        self.wave_writer = AudioWriter(self.phrases.keys())
        self.wave_reader = AudioReader(self.callback_wrapper)

        self.stop = StopState(self)
        self.record = RecordState(self)
        self.play = PlayState(self)
        self.switch = ExpressionState(self)

        self.active_state = self.stop
        self.control_on = False
        self.expression_on = False
        self.exp_on = False
        self.switch_on = False
        self.back_vol = 1
        self.program_on = False


    def callback_wrapper(self, in_data, frame_count, time_info, status):
        return self.callback(np.fromstring(in_data, dtype=np.int16), frame_count, time_info, status).astype(
            np.int16), pyaudio.paContinue

    def callback(self, in_data, frame_count, time_info, status):
        if self.active_state.name == "Stop":
            if self.active_state.auto_start_flag is True:
                if len(self.auto_start_threshold) > 0 and np.max(in_data) > 10  and np.mean(self.auto_start_threshold) < (np.max(in_data) /2) :
                    print("start auto recording")
                    self.active_state.auto_start_flag = False
                    self.auto_start_threshold = []
                    self.active_state = self.record
                elif np.max(in_data) > 10:
                    self.auto_start_threshold.append(np.max(in_data))
            return in_data
        if self.active_state.name in ["Play", "Expression"]:
            sample = self.active_phrase.phrase.counter(back_vol=self.back_vol)
            return sample + in_data
        if self.active_state.name == "Record":
            if self.active_phrase.is_overdubbing is True:
                if self.active_phrase.phrase.head == 0:
                    self.active_state = self.play
                sample = self.active_phrase.phrase.counter(in_data, back_vol=self.back_vol)
                self.active_phrase.overdub.put(in_data)
                return sample
            else:
                self.active_phrase.overdub.put(in_data)
                self.active_phrase.phrase.put(in_data)
                return in_data

    def on_midi(self, message, data):
        midi = message[0]
        self.timestamp += message[1]
        print("recieved message :%s at time %f" % (midi, self.timestamp))
        if midi[0] == 192:
            self.active_state.on_program_change(midi[1], timestamp=self.timestamp, time_delta=message[1], midi=midi)
        else:
            self.active_state.actions[midi[1]](midi[2], timestamp=self.timestamp, time_delta=message[1], midi=midi)
