from core.states import State


class PlayState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Play"

    def on_control(self, midi, phrase):
        print("Start OverDubbing")
        phrase.arm_overdubbing_track()
        self.session.active_state = self.session.record
        print("Finished prepadding overdub track OverDubbing")

    def on_long_control(self, midi, phrase):
        print("Stop Playing")
        self.session.active_state = self.session.stop

    def on_phrase_change(self, prev_patch, cur_patch, phrase):
        print("change phrase from %d to %d" % (prev_patch, cur_patch))
        phrase = self.session.phrases[cur_patch]

    def on_bank_down(self, prev_bank, cur_bank, phrase):
        print("Clear Layer")
        layers_left = phrase.clear_phrase()
        if layers_left == 0:
            self.session.active_state = self.session.stop

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        print("Select layer")
        phrase.select_phrase()

    def on_state(self, in_data, active_phrase):
        sample = active_phrase.phrase.counter(back_vol=self.back_vol)
        return sample + in_data
