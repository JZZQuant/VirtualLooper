from my_queue import IndexQueue as Queue
from states.State import State


class RecordState(State):
    def __init__(self,session):
        State.__init__(self,session)
        self.name = "Record"

    def on_control(self,value,timestamp,time_delta,midi):
        if time_delta < self.long_press_time and self.session.control_on:
            print("Started Looping")
            self.session.active_phrase.layers.append(self.session.active_phrase.overdub)
            self.session.active_phrase.overdub = Queue()
            self.session.active_state=self.session.play
        elif time_delta > self.long_press_time and self.session.control_on:
            print("Extend Recording")
            self.session.active_phrase.phrase.extend_loop()
            self.session.active_state=self.session.record
        self.session.control_on = ~self.session.control_on
