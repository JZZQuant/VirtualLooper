import queue
from states.State import State


class RecordState(State):
    def __init__(self,session):
        State.__init__(self,session)
        self.name = "Record"

    def on_control(self,value,timestamp,time_delta):
        if time_delta < 0.2 and self.session.control_on:
            print("Started Looping")
            self.session.active_phrase.layers.append(self.session.active_phrase.overdub)
            self.session.active_phrase.overdub = queue.Queue(maxsize=10000)
            self.session.active_state=self.session.play
        elif time_delta > 0.2 and self.session.control_on:
            print("Extend Recording")
            self.session.active_state=self.session.record
        self.session.control_on = ~self.session.control_on
