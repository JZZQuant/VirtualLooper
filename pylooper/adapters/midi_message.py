class MidiMessage(object):
    timestamp = 0
    long_press_time = 0.2

    def __init__(self, message):
        MidiMessage.timestamp += message[1]
        self.message = message[0]
        self.timestamp = MidiMessage.timestamp
        self.time_delta = message[1]
        if self.message[0] == 192:
            self.function = 0
            self.param = self.message[1]
        else:
            self.function = self.message[1]
            self.param = self.message[2]

    def is_bank_message(self):
        return self.message[1] == 0 and self.message[0] == 176

    def is_patch_message(self):
        return self.message[0] == 192

    def get_program_number(self, bank):
        return self.message[1] + bank * 100

    def get_bank_patch(self, program_number):
        return (program_number // 4) + 1, program_number % 4 + 1

    def is_short_press(self):
        return self.time_delta < MidiMessage.long_press_time
