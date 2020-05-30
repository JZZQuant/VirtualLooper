from states.State import State


class PlayState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Play"

    def on_control(self, value, timestamp, time_delta,midi):
        if time_delta < self.long_press_time and self.session.control_on:
            print("Start OverDubbing")
            self.session.active_phrase.is_overdubbing =True
            self.session.active_state = self.session.record
        elif time_delta > self.long_press_time and self.session.control_on:
            print("Stop Playing")
            self.session.active_state = self.session.stop
        self.session.control_on = ~self.session.control_on
