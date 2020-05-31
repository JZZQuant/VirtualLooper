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
            #postpend zeros to bring all layers to same length
            postpend_length = len(self.session.active_phrase.phrase.data) - len(self.session.active_phrase.overdub.data)
            self.session.active_phrase.overdub.data = self.session.active_phrase.overdub.data + postpend_length*[np.zeros(2*self.session.frames_per_buffer)]
            self.session.active_phrase.layers.append(self.session.active_phrase.overdub)
            for layer in self.session.active_phrase.layers:
                print(layer.data[0].shape)
            self.session.active_phrase.overdub = Queue()
            self.session.active_state=self.session.play
        elif time_delta > self.long_press_time and self.session.control_on:
            print("Extend Recording")
            self.session.active_phrase.phrase.extend_loop()
            self.session.active_state=self.session.record
        self.session.control_on = ~self.session.control_on

    def on_bank_up(self, prev_bank, cur_bank):
        print("setting auto stop flag")
        self.auto_stop_flag=True
