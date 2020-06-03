from core.states import State


class PlayState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = State.PLAY

    def on_control(self, midi, phrase):
        print("Start OverDubbing")
        # todo get rid of the callbak handler and forge it for now
        # todo : remove the session object permnently
        self.session.active_phrase.arm_overdubbing_track()
        print("Finished prepadding overdub track OverDubbing")
        return phrase.phrase_id, State.RECORD

    def on_long_control(self, midi, phrase):
        print("Stop Playing")
        return phrase.phrase_id, State.STOP

    def on_phrase_change(self, prev_patch, cur_patch, phrase):
        print("change phrase from %d to %d" % (prev_patch, cur_patch))
        return phrase.cur_patch, self.state_id

    def on_bank_down(self, prev_bank, cur_bank, phrase):
        print("Clear Layer")
        layers_left = self.session.active_phrase.clear_layer()
        if layers_left == 0:
            return phrase.phrase_id, State.STOP
        else:
            return phrase.phrase_id, self.state_id

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        print("Select layer")
        self.session.active_phrase.select_layer()

    def on_state(self, in_data, active_phrase):
        sample = active_phrase.phrase.counter(back_vol=self.back_vol)
        return sample + in_data
