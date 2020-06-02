import pyaudio


class State(object):
    def __init__(self, session):
        self.name = "Test"
        self.session = session
        self.long_press_time = 0.2
        self.midi_bank = 0
        self.curr_program = 0
        self.back_vol = 1
        self.control_on = False
        self.expression_on = False
        self.audio_writer = pyaudio.PyAudio()
        self.actions = {80: self.on_ctrl, 7: self.on_exp, 81: self.on_exp_switch, 32: self.dummy_func,
                        0: self.on_program_change}

    def dummy_func(self, midi):
        print("recieved control message")

    def on_ctrl(self, midi):
        if self.control_on:
            if midi.is_short_press():
                self.on_control(midi)
            else:
                self.on_long_control(midi)
        self.control_on = ~self.control_on

    def on_exp(self, midi):
        self.back_vol = midi.value / 100.0
        print("received exp message: %f" % self.back_vol)

    def on_exp_switch(self, midi):
        # suppress the midi off message and only recieve the on message
        if not midi.is_short_press():
            if not self.session.expression_on:
                if self.session.active_state.name == "Record":
                    self.session.active_phrase.close_recording_for_loop_over(self.session.frames_per_buffer)
                    self.session.active_state = self.session.switch
                self.session.write_phrases()
            else:
                self.session.active_state = self.session.play
            self.session.expression_on = ~self.session.expression_on
            print("received exp Switch message")

    def on_program_change(self, midi):
        if midi.is_bank_message():
            self.midi_bank = midi.param
        if midi.is_patch_message():
            prev_bank, prev_patch = midi.get_bank_patch(self.curr_program)
            self.curr_program = midi.get_program_number(self.midi_bank)
            cur_bank, cur_patch = midi.get_bank_patch(self.curr_program)
            if prev_bank == cur_bank:
                self.on_phrase_change(prev_patch, cur_patch)
            elif prev_bank > cur_bank:
                self.on_bank_down(prev_bank, cur_bank)
            else:
                self.on_bank_up(prev_bank, cur_bank)
            print("recieved program change message from %d,%d to %d,%d " % (prev_bank, prev_patch, cur_bank, cur_patch))

    def on_phrase_change(self, prev_patch, cur_patch):
        print("recieved phrase change message")

    def on_bank_down(self, prev_bank, cur_bank):
        print("recieved bank Down message")

    def on_bank_up(self, prev_bank, cur_bank):
        print("recieved bank up message message")

    def on_control(self, midi):
        print("recieved control message")

    def on_long_control(self, midi):
        print("recieved long control message")
