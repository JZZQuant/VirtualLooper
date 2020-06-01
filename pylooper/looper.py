from signal import pause

from adapters.midi import MidiDriver
from core.session import Session


class Looper(object):
    def __init__(self):
        midi_out = MidiDriver.get_midi_device_id(out=True)
        midi_in = MidiDriver.get_midi_device_id(out=False)
        self._sess = Session(midi_out, midi_in)

    def run(self):
        pause()


if __name__ == "__main__":
    looper = Looper()
    looper.run()
