import asyncio

import rtmidi

from Session import Session


class Looper(object):
    def __init__(self):
        self._sess = Session(1)
        self.timestamp=0

    def on_midi(self,message,data):
        midi = message[0]
        self.timestamp += message[1]
        print("recieved message :%s at time %f" % (midi,self.timestamp))
        print("current session : %s" % self._sess.active_phrase)

    async def start_session(self):
        midi_in = rtmidi.MidiIn()
        available_ports = midi_in.get_ports()

        for i, port in enumerate(available_ports, start=1):
            print("%d. Device: %s" % (i,port))

        print("Type the number corresponding to a device from above list : ")
        device_id = int(input())-1
        midi_in.open_port(device_id)
        print("Connected to device : %s" % available_ports[device_id])
        midi_in.set_callback(self.on_midi)

        await asyncio.Event().wait()

    def run(self):
        asyncio.run(self.start_session())

if __name__=="__main__":
    looper=Looper()
    looper.run()