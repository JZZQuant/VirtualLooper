from core.states import State


class PlayState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Play"

    def on_control(self, value, timestamp, time_delta,midi):
        if time_delta < self.long_press_time and self.session.control_on:
            print("Start OverDubbing")
            self.session.active_phrase.arm_overdubbing_track(self.session.frames_per_buffer)
            self.session.active_state = self.session.record
        elif time_delta > self.long_press_time and self.session.control_on:
            print("Stop Playing")
            self.session.active_state = self.session.stop
        self.session.control_on = ~self.session.control_on

    def on_phrase_change(self, prev_patch, cur_patch):
        self.session.active_phrase = self.session.phrases[cur_patch]

    def on_bank_down(self, prev_bank, cur_bank):
        print("Clear Layer")
        layers_left = self.session.active_phrase.clear_phrase()
        if layers_left == 0:
            self.session.active_state = self.session.stop

    def on_bank_up(self,prev_bank, cur_bank):
        print("Select layer")
        self.session.active_phrase.clear_phrase()
