from signal import pause

from adapters.midi import MidiDriver
from core.session import Session


class Looper(object):
    def __init__(self):
        midi_out = MidiDriver.get_midi_device_id(out=True)
        midi_in = MidiDriver.get_midi_device_id(out=False)
        self.auto_start_threshold = []
        self.midi_out = midi_out
        self.midi_in = midi_in
        midi = MidiDriver(midi_out, midi_in)
        self._sess = Session(midi)
        midi.midi_in.set_callback(self._sess.on_midi)

    def run(self):
        pause()


if __name__ == "__main__":
    looper = Looper()
    looper.run()
