import numpy as np

from core.states import State


class StopState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Stop"
        self.auto_start_flag = False
        self.auto_start_threshold = []

    def on_control(self, value, active_phrase):
        print("Started Recording")
        active_phrase.set_overdubbing_mode()
        return "Record"

    def on_long_control(self, value, active_phrase):
        # todo : must go back to void state which inherits from stop state
        if self.session.active_phrase.phrase.empty():
            print("No layers recorded for current phrase")
            return self.name
        else:
            print("Start Playing")
            return "Play"

    def on_phrase_change(self, prev_patch, cur_patch):
        print("change phrase from %d to %d" % (prev_patch, cur_patch))
        self.session.active_phrase = self.session.phrases[cur_patch]
        return self.name

    def on_bank_down(self, prev_bank, cur_bank):
        print("will roll start in now")

    def on_bank_up(self, prev_bank, cur_bank):
        print("setting auto start flag")
        self.auto_start_flag = True

    def on_state(self, in_data, active_phrase, back_vol):
        if self.auto_start_flag is True:
            if len(self.auto_start_threshold) > 0 and np.max(in_data) > 10 and np.mean(self.auto_start_threshold) < (
                    np.max(in_data) / 2):
                print("start auto recording")
                self.auto_start_flag = False
                self.auto_start_threshold = []
                return in_data, "Record"
            elif np.max(in_data) > 10:
                self.auto_start_threshold.append(np.max(in_data))
        return in_data, self.name
