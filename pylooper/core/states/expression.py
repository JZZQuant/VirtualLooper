import glob
import os

import numpy as np

from core.states import State


class ExpressionState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.state_id = State.EXPRESSION
        self.genres = dict(zip([1, 2, 3, 4], [x[0] for x in list(os.walk("../groove/"))][1:5]))
        self.active_genre = "jazz"
        self.active_loops = []
        self.loop_states = []
        self.active_loop_index = 0

    def on_state(self, in_data, active_phrase):
        sample = active_phrase.phrase.counter(back_vol=self.back_vol)
        return sample + in_data

    def on_phrase_change(self, prev_patch, cur_patch, phrase):
        self.set_rhythm_tracks(cur_patch)

    def set_rhythm_tracks(self, cur_patch):
        self.active_genre = self.genres[cur_patch]
        self.active_loops = [file for file in glob.glob(self.active_genre + '/beat/*.mid')]
        print(self.active_loops)
        self.loop_states = [-1] + list(range(len(self.active_loops)))

    def on_bank_down(self, prev_bank, cur_bank, phrase):
        self.on_bank_move(phrase, -1)

    def on_bank_up(self, prev_bank, cur_bank, phrase):
        self.on_bank_move(phrase, 1)

    def on_bank_move(self, phrase, iter):
        # todo : audio features can be replaced with  midi ?  reintrduced double half tempo,
        self.active_loop_index = (self.active_loop_index + iter) % (len(self.active_loops))
        # print("Current Selected Layer %s" % phrase_state)
        if self.active_loop_index == 0 and phrase.rhythm_appended is True:
            phrase.layers = phrase.layers[1:]
            phrase.rhythm_appended = False
        else:
            loop_name = self.active_loops[self.active_loop_index]
            print(loop_name)
            print(len(phrase.layers[0].data))
            rhythm_phrase = phrase.get_rhythm_phrase(loop_name, self.active_genre)
            if phrase.rhythm_appended is False:
                phrase.layers.insert(0, rhythm_phrase)
                phrase.rhythm_appended = True
            else:
                phrase.layers[0] = rhythm_phrase
        active_layers = [layer.data for layer in phrase.layers]
        phrase.phrase.data = list(np.array(active_layers).sum(axis=0))

    def on_control(self, midi, phrase):
        self.session.reset_session()

    def on_long_control(self, midi, phrase):
        if self.session.active_state.state_id == State.EXPRESSION:
            self.session.active_state = self.session.stop
        else:
            self.session.active_state = self.session.switch
