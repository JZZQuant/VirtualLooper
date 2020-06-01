from core.states import State


class StopState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Stop"

    def on_control(self, value, timestamp, time_delta,midi):
        print("Started Recording")
        self.session.active_phrase.set_overdubbing_mode()
        self.session.active_state = self.session.record

    def on_long_control(self, value, timestamp, time_delta, midi):
        if self.session.active_phrase.phrase.empty():
            print("No layers recorded for current phrase")
        else:
            print("Start Playing")
            self.session.active_state = self.session.play

    def on_phrase_change(self, prev_patch, cur_patch):
        self.session.active_phrase = self.session.phrases[cur_patch]

    def on_bank_down(self,prev_bank, cur_bank):
        print("will roll start in now")

    def on_bank_up(self, prev_bank, cur_bank):
        print("setting auto start flag")
        self.auto_start_flag=True
