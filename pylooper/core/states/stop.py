import numpy as np

from core.states import State


class StopState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.state_id = State.STOP
        self.auto_start_flag = False
        self.auto_start_threshold = []

    def on_control(self, midi, phrase):
        print("Started Recording")
        phrase.set_overdubbing_mode()
        self.session.active_state = self.session.record

    def on_long_control(self, midi, phrase):
        if phrase.phrase.empty():
            print("No layers recorded for current phrase")
        else:
            print("Start Playing")
            self.session.active_state = self.session.play

    def on_phrase_change(self, prev_patch, cur_patch, phrase):
        print("change phrase from %d to %d" % (prev_patch, cur_patch))
        phrase = self.session.phrases[cur_patch]

    def on_bank_down(self, prev_bank, cur_bank, phrase):
        print("will roll start in now")

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        print("setting auto start flag")
        self.auto_start_flag = True

    def on_state(self, in_data, active_phrase):
        if self.auto_start_flag is True:
            if len(self.auto_start_threshold) > 0 and np.max(in_data) > 10 and np.mean(self.auto_start_threshold) < (
                    np.max(in_data) / 2):
                print("start auto recording")
                self.auto_start_flag = False
                self.auto_start_threshold = []
                self.active_state = self.session.record
            elif np.max(in_data) > 10:
                self.auto_start_threshold.append(np.max(in_data))
        return in_data
