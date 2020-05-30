from states.State import State


class StopState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Stop"

    def on_control(self, value, timestamp, time_delta):
        if time_delta < 0.2 and self.session.control_on:
            # go to the active phrase,start playing in loop from queue
            print("Started Recording")
            self.session.active_phrase.is_overdubbing = ~self.session.active_phrase.phrase.empty()
            self.session.active_state = self.session.record
        elif time_delta > 0.2 and self.session.control_on:
            print("Start Playing")
            self.session.active_state = self.session.play
        self.session.control_on = ~self.session.control_on
