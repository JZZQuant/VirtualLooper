import numpy as np

from core.states import State


class PlayState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Play"

    def on_control(self, value, timestamp, time_delta,midi):
        if time_delta < self.long_press_time and self.session.control_on:
            print("Start OverDubbing")
            #prepend zeros before the layer begines
            base_layer = self.session.active_phrase.phrase
            self.session.active_phrase.overdub.pre_padding(base_layer.head*[np.zeros(2*self.session.frames_per_buffer)])
            self.session.active_phrase.is_overdubbing =True
            self.session.active_state = self.session.record
        elif time_delta > self.long_press_time and self.session.control_on:
            print("Stop Playing")
            self.session.active_state = self.session.stop
        self.session.control_on = ~self.session.control_on

    def on_phrase_change(self, prev_patch, cur_patch):
        self.session.active_phrase = self.session.phrases[cur_patch]

    def on_bank_down(self, prev_bank, cur_bank):
        print("Clear Layer")
        n = len(self.session.active_phrase.layers)
        phrase_state = self.session.active_phrase.phrase_states()[self.session.active_phrase.phrase_state_index]
        self.session.active_phrase.layers = [self.session.active_phrase.layers[i] for i in range(n) if i not in phrase_state]
        self.session.active_phrase.phrase_state_index = 0
        if self.session.active_phrase.layers != []:
            active_layers = [layer.data for layer in self.session.active_phrase.layers]
            self.session.active_phrase.phrase.data = list(np.array(active_layers).sum(axis=0))
        else:
            self.session.active_phrase.__init__()
            self.session.active_state = self.session.stop

    def on_bank_up(self,prev_bank, cur_bank):
        print("Select layer")
        self.session.active_phrase.phrase_state_index = (self.session.active_phrase.phrase_state_index + 1)%(len(self.session.active_phrase.layers)+1)
        phrase_state = self.session.active_phrase.phrase_states()[self.session.active_phrase.phrase_state_index]
        print(phrase_state)
        active_layers = [self.session.active_phrase.layers[i].data for i in phrase_state]
        self.session.active_phrase.phrase.data = list(np.array(active_layers).sum(axis=0))
