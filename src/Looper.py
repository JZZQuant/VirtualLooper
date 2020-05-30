import asyncio
import rtmidi
from Session import Session


class Looper(object):
    def __init__(self):
        self.midi_in = rtmidi.MidiIn().open_port(0)
        # self.midi_in = self.get_midi_in()
        self._sess = Session(1, self)
        self.timestamp = 0

    def get_midi_in(self):
        midi_in = rtmidi.MidiIn()
        available_ports = midi_in.get_ports()
        for i, port in enumerate(available_ports, start=1):
            print("%d. Device: %s" % (i, port))
        print("Type the number corresponding to a device from above list : ")
        device_id = int(input()) - 1
        midi_in.open_port(device_id)
        print("Connected to device : %s" % available_ports[device_id])
        return midi_in

    def get_midi_out(self):
        midi_out = rtmidi.MidiOut()
        available_ports = midi_out.get_ports()
        for i, port in enumerate(available_ports, start=1):
            print("%d. Device: %s" % (i, port))
        print("Type the number corresponding to a device from above list : ")
        device_id = int(input()) - 1
        midi_out.open_port(device_id)
        print("Connected to device : %s" % available_ports[device_id])
        return midi_out

    def on_midi(self, message, data):
        midi = message[0]
        self.timestamp += message[1]
        print("recieved message :%s at time %f" % (midi, self.timestamp))
        self._sess.active_state.actions[midi[1]](midi[2], timestamp=self.timestamp, time_delta=message[1])

    async def start_session(self):
        self.midi_in.set_callback(self.on_midi)
        await asyncio.Event().wait()

    def run(self):
        asyncio.run(self.start_session(), debug=True)


if __name__ == "__main__":
    looper = Looper()
    looper.run()
