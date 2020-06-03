import pyaudio


class State(object):
    STOP = "Stop"
    RECORD = "Record"
    PLAY = "Play"
    EXPRESSION = "Expression"
    VOID = "Void"

    def __init__(self, session):
        self.state_id = State.VOID
        self.session = session
        self.midi_bank = 0
        self.program = 0
        self.back_vol = 1
        # control actions like raising pedal are taken after foot is raised , so we count only control off
        self.control_off = False
        self.expression_on = False
        self.audio_writer = pyaudio.PyAudio()
        # todo : requires enums or other place holders to avoid loose numbers
        self.actions = {80: self.on_ctrl, 7: self.on_exp, 81: self.on_exp_switch, 32: self.dummy_func,
                        0: self.on_program_change}

    def dummy_func(self, midi, phrase):
        print("recieved control message")
        return phrase.phrase_id, self.state_id

    def on_ctrl(self, midi, phrase):
        self.control_off = ~self.control_off
        if not self.control_off:
            if midi.is_short_press():
                return self.on_control(midi, phrase)
            else:
                return self.on_long_control(midi, phrase)

    def on_exp(self, midi, phrase):
        self.back_vol = midi.value / 100.0
        print("received exp message: %f" % self.back_vol)
        return phrase.phrase_id, self.state_id

    def on_exp_switch(self, midi, phrase):
        # suppress the midi off message and only recieve the on message
        if not midi.is_short_press():
            self.expression_on = ~self.expression_on
            print("received exp Switch message")
            if self.expression_on:
                if self.state_id == State.RECORD:
                    self.session.active_phrase.close_recording_for_loop_over()
                    return phrase.phrase_id, State.EXPRESSION
                return phrase.phrase_id, self.EXPRESSION
            else:
                return phrase.phrase_id, State.PLAY

    def on_program_change(self, midi, phrase):
        if midi.is_bank_message():
            self.midi_bank = midi.param
        if midi.is_patch_message():
            prev_bank, prev_patch = midi.get_bank_patch(self.program)
            self.program = midi.get_program_number(self.midi_bank)
            cur_bank, cur_patch = midi.get_bank_patch(self.program)
            print("recieved program change message from %d,%d to %d,%d " % (prev_bank, prev_patch, cur_bank, cur_patch))
            if prev_bank == cur_bank:
                return self.on_phrase_change(prev_patch, cur_patch, phrase)
            elif prev_bank > cur_bank:
                return self.on_bank_down(prev_bank, cur_bank, phrase)
            else:
                return self.on_bank_up(prev_bank, cur_bank, phrase)

    def on_phrase_change(self, prev_patch, cur_patch, phrase):
        print("recieved phrase change message")

    def on_bank_down(self, prev_bank, cur_bank, phrase):
        print("recieved bank Down message")

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        print("recieved bank up message message")

    def on_control(self, midi, phrase):
        print("recieved control message")

    def on_long_control(self, midi, phrase):
        print("recieved long control message")
