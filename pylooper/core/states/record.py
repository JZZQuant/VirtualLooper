from core.states import State


class RecordState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Record"

    def on_control(self, value, timestamp, time_delta, midi):
        if time_delta < self.long_press_time and self.session.control_on:
            print("Started Looping")
            self.session.active_phrase.close_recording_for_loop_over(self.session.frames_per_buffers)
            self.session.active_state = self.session.play
        elif time_delta > self.long_press_time and self.session.control_on:
            print("Extend Recording")
            self.session.active_phrase.extend_recording()
            self.session.active_state=self.session.record
        self.session.control_on = ~self.session.control_on

    def on_bank_up(self, prev_bank, cur_bank):
        print("still Unimplemented feature flag")
