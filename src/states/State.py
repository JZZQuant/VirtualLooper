class State(object):
    def __init__(self,session):
        self.name = "Test"
        self.session=session
        self.long_press_time = 0.2
        self.midi_bank = 0
        self.curr_program = 0
        self.actions={80:self.on_control,7:self.on_exp,81:self.on_exp_switch,32:lambda x : "Hello World",0:self.on_program_change}

    def on_control(self,value,timestamp,time_delta,midi):
        print("recieved control message")

    def on_exp(self,value,timestamp,time_delta,midi):
        print("recieved exp message")

    def on_exp_switch(self,value,timestamp,time_delta,midi):
        print("recieved exp Switch message")

    def on_program_change(self,value,timestamp,time_delta,midi):
        if midi[1] == 0 and midi[0] == 176:
            self.midi_bank = midi[2]
        if midi[1] == 192:
            self.curr_program = midi[1] + self.midi_bank*100
        print("recieved program change message")