import numpy as np

from my_queue import IndexQueue as Queue
from states.State import State


class RecordState(State):
    def __init__(self,session):
        State.__init__(self,session)
        self.name = "Record"

    def on_control(self,value,timestamp,time_delta,midi):
        if time_delta < self.long_press_time and self.session.control_on:
            print("Started Looping")
            max_size = max([len(layer.data) for layer in self.session.active_phrase.layers] + [len(self.session.active_phrase.phrase.data)])
            self.session.active_phrase.max_size = max_size
            #postpend zeros to bring all layers to same length
            postpend_length = len(self.session.active_phrase.phrase.data) - len(self.session.active_phrase.overdub.data)
            self.session.active_phrase.overdub.post_padding(postpend_length*[np.zeros(2*self.session.frames_per_buffer)])
            self.session.active_phrase.layers.append(self.session.active_phrase.overdub.slice(max_size))
            self.session.active_phrase.overdub = Queue(max_size= max_size)
            self.session.active_state=self.session.play
        elif time_delta > self.long_press_time and self.session.control_on:
            print("Extend Recording")
            self.session.active_phrase.phrase.extend_loop()
            for layer in self.session.active_phrase.layers:
                layer.extend_loop()
            self.session.active_state=self.session.record
        self.session.control_on = ~self.session.control_on

    def on_bank_up(self, prev_bank, cur_bank):
        print("still Unimplemented feature flag")
