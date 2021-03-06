from core.states import State


class RecordState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.state_id = State.RECORD
        self.auto_stop = False

    def on_control(self, midi, phrase):
        print("Started Looping")
        phrase.close_recording_for_loop_over()
        self.session.active_state = self.session.play

    def on_long_control(self, midi, phrase):
        print("Extend Recording")
        phrase.extend_recording()
        self.session.active_state = self.session.record

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        self.auto_stop = True

    def on_state(self, in_data, active_phrase):
        if active_phrase.is_overdubbing is True:
            if active_phrase.phrase.head == 0:
                print("Finished recording force set overdubbing to play mode")
                active_phrase.close_recording_for_loop_over()
                if self.auto_stop:
                    self.session.active_state = self.session.stop
                else:
                    self.session.active_state = self.session.play
            sample = active_phrase.phrase.counter(in_data, back_vol=self.back_vol)
            active_phrase.overdub.put(in_data)
            return sample
        else:
            active_phrase.overdub.put(in_data)
            active_phrase.phrase.put(in_data)
            return in_data
