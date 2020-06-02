from core.states import State


class RecordState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Record"

    def on_control(self, value, active_phrase):
        print("Started Looping")
        self.session.active_phrase.close_recording_for_loop_over()
        # todo replace all these to enums
        return "Play"

    def on_long_control(self, value, timestamp):
        print("Extend Recording")
        self.session.active_phrase.extend_recording()
        return "Record"

    def on_bank_up(self, prev_bank, cur_bank):
        print("still Unimplemented feature flag")

    def on_state(self, in_data, active_phrase, back_vol):
        if active_phrase.is_overdubbing is True:
            sample = active_phrase.phrase.counter(in_data, back_vol=back_vol)
            active_phrase.overdub.put(in_data)
            if active_phrase.phrase.head == 0:
                print("Finished recording force set overdubbing to play mode")
                active_phrase.close_recording_for_loop_over()
                return sample, "Play"
            return sample, self.name
        else:
            active_phrase.overdub.put(in_data)
            active_phrase.phrase.put(in_data)
            return in_data, self.name
