from core.states import State


class StopState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Stop"

    def on_control(self, value, timestamp, time_delta,midi):
        if time_delta < self.long_press_time and self.session.control_on:
            # go to the active phrase,start playing in loop from queue
            print("Started Recording")
            self.session.active_phrase.is_overdubbing = ~self.session.active_phrase.phrase.empty()
            self.session.active_state = self.session.record
        elif time_delta > self.long_press_time and self.session.control_on and not self.session.active_phrase.phrase.empty():
            print("Start Playing")
            self.session.active_state = self.session.play
        self.session.control_on = ~self.session.control_on

    def on_phrase_change(self, prev_patch, cur_patch):
        self.session.active_phrase = self.session.phrases[cur_patch]

    def on_bank_down(self,prev_bank, cur_bank):
        print("will roll start in now")

    def on_bank_up(self, prev_bank, cur_bank):
        print("setting auto start flag")
        self.auto_start_flag=True
