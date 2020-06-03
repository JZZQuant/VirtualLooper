import numpy as np

from core.states import State


class StopState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = State.STOP
        self.auto_start_flag = False
        self.auto_start_threshold = []

    def on_control(self, midi, phrase):
        print("Started Recording")
        self.session.active_phrase.set_overdubbing_mode()
        return phrase.phrase_id, State.RECORD

    def on_long_control(self, midi, phrase):
        if self.session.active_phrase.phrase.empty():
            print("No layers recorded for current phrase")
            return phrase.phrase_id, self.state_id
        else:
            print("Start Playing")
            return phrase.phrase_id, State.PLAY

    def on_phrase_change(self, prev_patch, cur_patch, phrase):
        print("change phrase from %d to %d" % (prev_patch, cur_patch))
        return cur_patch, self.state_id

    def on_bank_down(self, prev_bank, cur_bank, phrase):
        print("will roll start in now")

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        print("setting auto start flag")
        self.auto_start_flag = True
        return phrase.phrase_id, self.state_id

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
