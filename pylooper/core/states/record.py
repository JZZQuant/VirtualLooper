from core.states import State


class RecordState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.state_id = State.RECORD

    def on_control(self, midi, phrase):
        print("Started Looping")
        self.session.active_phrase.close_recording_for_loop_over()
        return phrase.phrase_id, State.PLAY

    def on_long_control(self, midi, phrase):
        print("Extend Recording")
        self.session.active_phrase.extend_recording()
        return phrase.phrase_id, State.RECORD

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        print("still Unimplemented feature flag")

    def on_state(self, in_data, active_phrase):
        # todo : need to implement state change for on_state as well
        if active_phrase.is_overdubbing is True:
            if active_phrase.phrase.head == 0:
                print("Finished recording force set overdubbing to play mode")
                active_phrase.close_recording_for_loop_over()
                self.session.active_state = self.session.play
            sample = active_phrase.phrase.counter(in_data, back_vol=self.back_vol)
            active_phrase.overdub.put(in_data)
            return sample
        else:
            active_phrase.overdub.put(in_data)
            active_phrase.phrase.put(in_data)
            return in_data
