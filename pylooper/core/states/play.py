from core.states import State


class PlayState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Play"

    def on_control(self, value, timestamp, time_delta, midi):
        print("Start OverDubbing")
        self.session.active_phrase.arm_overdubbing_track()
        self.session.active_state = self.session.record
        print("Finished prepadding overdub track OverDubbing")

    def on_long_control(self, value, timestamp, time_delta, midi):
        print("Stop Playing")
        self.session.active_state = self.session.stop

    def on_phrase_change(self, prev_patch, cur_patch):
        print("change phrase from %d to %d" % (prev_patch, cur_patch))
        self.session.active_phrase = self.session.phrases[cur_patch]

    def on_bank_down(self, prev_bank, cur_bank):
        print("Clear Layer")
        layers_left = self.session.active_phrase.clear_phrase()
        # todo : must go back to void state which inherits from stop state
        if layers_left == 0:
            self.session.active_state = self.session.stop

    def on_bank_up(self, prev_bank, cur_bank):
        print("Select layer")
        self.session.active_phrase.select_phrase()

    def on_state(self, in_data, active_phrase, back_vol):
        sample = active_phrase.phrase.counter(back_vol=back_vol)
        return sample + in_data
