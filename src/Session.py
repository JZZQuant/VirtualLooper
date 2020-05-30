from my_queue import IndexQueue as Queue
import numpy as np
from states.PlayState import PlayState
from states.RecordState import RecordState
from states.State import State
from states.StopState import StopState
import pyaudio


class Phrase(object):
    def __init__(self):
        self.is_overdubbing = False
        self.phrase = Queue()
        self.overdub = Queue()
        self.layers = []


class Session(object):
    def __init__(self, active_phrase, looper):
        self.phrases = {1: Phrase(), 2: Phrase(), 3: Phrase(), 4: Phrase()}
        self.active_phrase = self.phrases[active_phrase]
        self.stop = StopState(self)
        self.record = RecordState(self)
        self.play = PlayState(self)
        self.switch = State(self)
        self.active_state = self.stop
        self.control_on = False
        self.exp_on = False
        self.switch_on = False
        self.back_vol = 1
        self.program_on = False
        self.looper = looper
        self.sound = Queue()
        stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=2, output=True, rate=44100, input=True,
                                        frames_per_buffer=1024, stream_callback=self.callback_wrapper)

    def callback_wrapper(self, in_data, frame_count, time_info, status):
        return self.callback(np.fromstring(in_data, dtype=np.int16), frame_count, time_info, status).astype(
            np.int16), pyaudio.paContinue

    def callback(self, in_data, frame_count, time_info, status):
        if self.active_state.name == "Stop":
            return in_data
        if self.active_state.name == "Play":
            # print("playing")
            sample = self.active_phrase.phrase.counter(back_vol=self.back_vol)
            return sample + in_data
        if self.active_state.name == "Record":
            if self.active_phrase.is_overdubbing is True:
                # print("overdubbing")
                sample = self.active_phrase.phrase.counter(in_data,back_vol=self.back_vol)
                self.active_phrase.overdub.put(in_data)
                return sample
            else:
                # print("recording")
                self.active_phrase.overdub.put(in_data)
                self.active_phrase.phrase.put(in_data)
                return in_data
