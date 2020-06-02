class State(object):
    def __init__(self, session):
        self.name = "Test"
        self.session = session
        self.long_press_time = 0.2
        self.midi_bank = 0
        self.curr_program = 0
        self.actions = {80: self.on_ctrl, 7: self.on_exp, 81: self.on_exp_switch, 32: self.dummy_func,
                        0: self.on_program_change}

    def dummy_func(self, value, active_phrase, time_delta, midi):
        print("recieved control message")

    def on_ctrl(self, value, active_phrase, time_delta, midi):
        if time_delta < self.long_press_time and self.session.control_on:
            self.on_control(value, active_phrase)
        elif time_delta > self.long_press_time and self.session.control_on:
            self.on_long_control(value, active_phrase)
        self.session.control_on = ~self.session.control_on

    def on_exp(self, value, active_phrase, time_delta, midi):
        self.session.back_vol = value / 100.0
        print("received exp message: %f" % self.session.back_vol)

    def on_exp_switch(self, value, active_phrase, time_delta, midi):
        # suppress the midi off message and only recieve the on message
        if time_delta > self.long_press_time:
            print("received exp Switch message")
            # todo : change this to a more abstract pedal on/off
            if not self.session.expression_on:
                if self.name == "Record":
                    active_phrase.close_recording_for_loop_over()
                    return "Rhythm"
                # todo :move this to session after recieveing reset call
                # self.session.write_phrases()
            else:
                return "Play"
            self.session.expression_on = ~self.session.expression_on

    def on_program_change(self, value, active_phrase, time_delta, midi):
        if midi[1] == 0 and midi[0] == 176:
            self.midi_bank = midi[2]
        if midi[0] == 192:
            temp = self.curr_program
            self.curr_program = midi[1] + self.midi_bank * 100
            prev_bank, prev_patch = (temp // 4) + 1, temp % 4 + 1
            cur_bank, cur_patch = (self.curr_program // 4) + 1, self.curr_program % 4 + 1
            if prev_bank == cur_bank:
                self.on_phrase_change(prev_patch, cur_patch, active_phrase)
            elif prev_bank > cur_bank:
                self.on_bank_down(prev_bank, cur_bank, active_phrase)
            else:
                self.on_bank_up(prev_bank, cur_bank, active_phrase)
            print("recieved program change message from %d,%d to %d,%d " % (prev_bank, prev_patch, cur_bank, cur_patch))

    def on_phrase_change(self, prev_patch, cur_patch, active_phrase):
        print("recieved phrase change message")

    def on_bank_down(self, prev_bank, cur_bank, active_phrase):
        print("recieved bank Down message")

    def on_bank_up(self, prev_bank, cur_bank, active_phrase):
        print("recieved bank up message message")

    def on_control(self, value, active_phrase):
        print("recieved control message")

    def on_long_control(self, value, active_phrase):
        print("recieved long control message")
