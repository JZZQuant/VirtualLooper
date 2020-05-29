class Phrase(object):
    pass

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


class StopState(State):
    def __init__(self,session):
        State.__init__(self,session)
        self.name = "Stop"

    def on_control(self,value,timestamp,time_delta):
        if time_delta < 0.2 and self.session.control_on:
            print("Started Recording")
            self.session.active_state=self.session.record
        elif time_delta > 0.2 and self.session.control_on:
            print("Start Playing")
            self.session.active_state=self.session.play
        self.session.control_on = ~self.session.control_on


class RecordState(State):
    def __init__(self,session):
        State.__init__(self,session)
        self.name = "Record"

    def on_control(self,value,timestamp,time_delta):
        if time_delta < 0.2 and self.session.control_on:
            print("Started Looping")
            self.session.active_state=self.session.play
        elif time_delta > 0.2 and self.session.control_on:
            print("Extend Recording")
            self.session.active_state=self.session.record
        self.session.control_on = ~self.session.control_on


class PlayState(State):
    def __init__(self,session):
        State.__init__(self,session)
        self.name = "Play"

    def on_control(self,value,timestamp,time_delta):
        if time_delta < 0.2 and self.session.control_on:
            print("Start OverDubbing")
            self.session.active_state=self.session.record
        elif time_delta > 0.2 and self.session.control_on:
            print("Stop Playing")
            self.session.active_state=self.session.stop
        self.session.control_on = ~self.session.control_on


class Session(object):
    def __init__(self,active_phrase):
        self.phrases = {1:Phrase(),2:Phrase(),3:Phrase(),4:Phrase()}
        self.active_phrase=self.phrases[active_phrase]
        self.stop=StopState(self)
        self.record= RecordState(self)
        self.play=PlayState(self)
        self.switch=State(self)
        self.active_state = self.stop
        self.control_on=False
        self.exp_on=False
        self.switch_on=False
        self.program_on=False

