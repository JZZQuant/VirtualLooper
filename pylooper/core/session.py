import os
import uuid

import numpy as np
import pyaudio

from core import *
from structures.pile_queue import Queue


class Phrase(object):
    def __init__(self):
        self.is_overdubbing = False
        self.phrase = Queue()
        self.overdub = Queue()
        self.layers = []
        self.phrase_state_index = -1

    def phrase_states(self):
        n = len(self.layers)
        return [list(range(n))] + [[el] for el in range(n)]


class Session(object):
    def __init__(self, active_phrase, looper):
        self.auto_start_threshold = []
        self.phrases = {1: Phrase(), 2: Phrase(), 3: Phrase(), 4: Phrase()}
        self.active_phrase = self.phrases[active_phrase]
        self.session_id = str(uuid.uuid4())
        self.folder = "../../VLoop/" + self.session_id
        for i in self.phrases.keys():
            os.makedirs(self.folder + "/phrase" + str(i) + "/")
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
        self.looper = looper
        self.sound = Queue()
        self.frames_per_buffer = 256
        self.sample_rate = 44100
        self.channels = 2
        stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=self.channels, output=True,
                                        rate=self.sample_rate, input=True,
                                        frames_per_buffer=self.frames_per_buffer, stream_callback=self.callback_wrapper)

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
