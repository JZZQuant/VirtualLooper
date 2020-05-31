import os
import wave

import pyaudio

from my_queue import IndexQueue as Queue


class State(object):
    def __init__(self, session):
        self.name = "Test"
        self.session = session
        self.long_press_time = 0.2
        self.midi_bank = 0
        self.curr_program = 0
        self.auto_start_flag =False
        self.auto_stop_flag =False
        self.audio_writer = pyaudio.PyAudio()
        self.actions = {80: self.on_control, 7: self.on_exp, 81: self.on_exp_switch, 32: lambda x: "Hello World",
                        0: self.on_program_change}

    def on_control(self, value, timestamp, time_delta, midi):
        print("recieved control message")

    def on_exp(self, value, timestamp, time_delta, midi):
        self.session.back_vol = value / 100.0
        print("received exp message: %f" % self.session.back_vol)

    def on_exp_switch(self, value, timestamp, time_delta, midi):
        if time_delta > self.long_press_time:
            if not self.session.expression_on:
                if self.session.active_state.name == "Record":
                    self.session.active_phrase.layers.append(self.session.active_phrase.overdub)
                    self.session.active_phrase.overdub = Queue()
                    self.session.active_state = self.session.switch
                for i, phrase in self.session.phrases.items():
                    if len(phrase.layers) == 0:
                        pass
                    for layer in phrase.layers:
                        file_name = self.session.folder + "/phrase" + str(i) + "/" + str(hash(str(layer.data[0]))) + ".wav"
                        if not os.path.exists(file_name):
                            with wave.open(file_name, 'wb') as wf:
                                wf.setnchannels(self.session.channels)
                                wf.setsampwidth(2)
                                wf.setframerate(self.session.sample_rate)
                                wf.writeframes(b''.join(layer.data))
            else:
                self.session.active_state = self.session.play
            self.session.expression_on = ~self.session.expression_on
            print("received exp Switch message")

    def on_program_change(self, value, timestamp, time_delta, midi):
        if midi[1] == 0 and midi[0] == 176:
            self.midi_bank = midi[2]
        # todo : change it back to midi 1 after testing is over
        if midi[0] == 192:
            temp = self.curr_program
            self.curr_program = midi[1] + self.midi_bank * 100
            prev_bank,prev_patch =  temp/4,temp%4
            cur_bank,cur_patch =  self.curr_program/4,self.curr_program%4
            if prev_bank == cur_bank:
                self.on_phrase_change(prev_patch,cur_patch)
            elif prev_bank > cur_bank :
                self.on_bank_down(prev_bank,cur_bank)
            else :
                self.on_bank_up(prev_bank,cur_bank)
            print("recieved program change message from %d,%d to %d,%d " % (prev_bank,prev_patch,cur_bank,cur_patch))

    def on_phrase_change(self, prev_patch, cur_patch):
        print("recieved phrase change message")

    def on_bank_down(self, prev_bank, cur_bank):
        print("recieved bank Down message")

    def on_bank_up(self,prev_bank, cur_bank):
        print("recieved bank up message message")
