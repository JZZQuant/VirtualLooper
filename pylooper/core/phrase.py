import numpy as np

from structures import Queue


class Phrase(object):
    def __init__(self):
        self.is_overdubbing = False
        self.phrase = Queue()
        self.overdub = Queue()
        self.layers = []
        self.phrase_state_index = -1

    def phrase_states(self):
        n = len(self.layers)
        return [list(range(n))] + [[el] for el in range(n)]

    def arm_overdubbing_track(self, buffer_rate):
        self.overdub.pre_padding(self.phrase.head * [np.zeros(2 * buffer_rate)])
        self.is_overdubbing = True

    def clear_phrase(self):
        n = len(self.layers)
        phrase_state = self.phrase_states()[self.phrase_state_index]
        self.layers = [self.layers[i] for i in range(n) if i not in phrase_state]
        self.phrase_state_index = 0
        if self.layers != []:
            active_layers = [layer.data for layer in self.layers]
            self.phrase.data = list(np.array(active_layers).sum(axis=0))
        else:
            self.__init__()
        return len(self.layers)

    def select_phrase(self):
        self.phrase_state_index = (self.phrase_state_index + 1) % (len(self.layers) + 1)
        phrase_state = self.phrase_states()[self.phrase_state_index]
        active_layers = [self.layers[i].data for i in phrase_state]
        self.phrase.data = list(np.array(active_layers).sum(axis=0))

    def close_recording_for_loop_over(self, buffer_rate):
        max_size = max([len(layer.data) for layer in self.layers] + [len(self.phrase.data)])
        self.max_size = max_size
        # postpend zeros to bring all layers to same length
        postpend_length = len(self.phrase.data) - len(self.overdub.data)
        self.overdub.post_padding(postpend_length * [np.zeros(2 * buffer_rate)])
        self.layers.append(self.overdub.slice(max_size))
        self.overdub = Queue()

    def extend_recording(self):
        self.phrase.extend_loop()
        for layer in self.layers:
            layer.extend_loop()

    def set_overdubbing_mode(self):
        # set to overdubbing if phrase is not empty else set to first recording
        self.is_overdubbing = ~self.phrase.empty()
