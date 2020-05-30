class State(object):
    def __init__(self,session):
        self.name = "Test"
        self.session=session
        self.actions={80:self.on_control,7:self.on_exp,81:self.on_exp_switch,32:lambda x : "Hello World",0:self.on_program_change}

    def on_control(self,value,timestamp,time_delta):
        print("recieved control message")

    def on_exp(self,value,timestamp,time_delta):
        print("recieved exp message")

    def on_exp_switch(self,value,timestamp,time_delta):
        print("recieved exp Switch message")

    def on_program_change(self,value,timestamp,time_delta):
        print("recieved program change message")