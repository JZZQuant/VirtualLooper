
import time
import rtmidi

midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()

if 'VMPK Output' in available_ports:
    midi_in.open_port(available_ports.index('VMPK Output'))


midi_in.set_callback(lambda x: print(str(x)+ str(y)))



