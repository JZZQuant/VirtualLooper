import rtmidi


class MidiDriver(object):
    active_phrase = 0

    def __init__(self, midi_out, midi_in, active_phrase=1):
        self.midi_in = rtmidi.MidiIn().open_port(midi_in)
        self.midi_out = rtmidi.MidiOut().open_port(midi_out)
        MidiDriver.active_phrase = active_phrase
        self.send1()

    def send1(self):
        self.midi_out.send_message([176, 0, 0])
        self.midi_out.send_message([176, 32, 0])
        self.midi_out.send_message([192, MidiDriver.active_phrase - 1])

    @staticmethod
    def get_midi_device_id(out=True):
        device_id, available_ports = MidiDriver.get_default_device_id(out=True)
        if device_id < 0:
            device_id = MidiDriver.ask_user_for_device_id(available_ports)
        return device_id

    @staticmethod
    def ask_user_for_device_id(available_ports):
        for i, port in enumerate(available_ports, start=1):
            print("%d. Device: %s" % (i, port))
        print("Type the number corresponding to a device from above list : ")
        device_id = int(input()) - 1
        return device_id

    @staticmethod
    def get_default_device_id(out=True):
        device_id = -1
        midi = rtmidi.MidiOut() if out else rtmidi.MidiIn()
        available_ports = midi.get_ports()
        available_ports = [port.lower() for port in available_ports]
        for device_name in ["uno", "vmpk"]:
            for port in available_ports:
                if device_name in port:
                    device_id = available_ports.index(port)
        return device_id, available_ports
