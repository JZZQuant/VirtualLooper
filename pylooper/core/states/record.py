from core.states import State


class RecordState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Record"

    def on_control(self, value, timestamp, time_delta, midi):
        print("Started Looping")
        self.session.active_phrase.close_recording_for_loop_over(self.session.wave_reader.frames_per_buffer)
        self.session.active_state = self.session.play

    def on_long_control(self, value, timestamp, time_delta, midi):
        print("Extend Recording")
        self.session.active_phrase.extend_recording()
        self.session.active_state=self.session.record
        self.session.control_on = ~self.session.control_on

    def on_bank_up(self, prev_bank, cur_bank):
        print("still Unimplemented feature flag")
