class Phrase(object):
    pass


class Session(object):
    def __init__(self,active_phrase):
        self.phrases = {1:Phrase(),2:Phrase(),3:Phrase(),4:Phrase()}
        self.active_phrase=self.phrases[active_phrase]
        # self.event=event
        # define state objects here each of which has a copy of the session object to mess around with
