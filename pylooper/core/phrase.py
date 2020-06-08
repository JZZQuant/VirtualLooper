import numpy
import numpy as np
import pywt
from midi2audio import FluidSynth
from mido import MidiFile
from scipy import signal
from scipy.io import wavfile

from structures import Queue


class Phrase(object):
    def __init__(self, channels, buffer_rate, sample_rate, phrase_id):
        self.is_overdubbing = False
        self.phrase_id = phrase_id
        self.phrase = Queue()
        self.overdub = Queue()
        self.layers = []
        self.number_of_channels = channels
        self.frames_per_buffer = buffer_rate
        self.sample_rate = sample_rate
        self.phrase_state_index = -1
        self.rhythm_appended = False
        self.tempo = 120
        self.beats = []
        self.offset = 0

    def phrase_states(self):
        n = len(self.layers)
        return [list(range(n))] + [[el] for el in range(n)]

    def set_tempo(self):
        flattened_array_y = np.array(self.layers[0].data).flatten()
        self.tempo, self.beats = bpm_detector(flattened_array_y, self.sample_rate)
        # self.tempo, self.beats = librosa.beat.beat_track(y=flattened_array_y, sr=self.sample_rate, units="frames")

    def arm_overdubbing_track(self):
        print("Pre-padding records with zeros")
        self.overdub.pre_padding(self.phrase.head * [np.zeros(self.number_of_channels * self.frames_per_buffer)])
        self.is_overdubbing = True

    def clear_phrase(self):
        n = len(self.layers)
        phrase_state = self.phrase_states()[self.phrase_state_index]
        print("found %d layers clearing %s from it" % (n, phrase_state))
        self.layers = [self.layers[i] for i in range(n) if i not in phrase_state]
        self.phrase_state_index = 0
        if self.layers:
            active_layers = [layer.data for layer in self.layers]
            self.phrase.data = list(np.array(active_layers).sum(axis=0))
        else:
            self.__init__(self.number_of_channels, self.frames_per_buffer, self.sample_rate, self.phrase_id)
        return len(self.layers)

    def select_phrase(self):
        self.phrase_state_index = (self.phrase_state_index + 1) % (len(self.layers) + 1)
        phrase_state = self.phrase_states()[self.phrase_state_index]
        print("Current Selected Layer %s" % phrase_state)
        active_layers = [self.layers[i].data for i in phrase_state]
        self.phrase.data = list(np.array(active_layers).sum(axis=0))

    def close_recording_for_loop_over(self):
        print("post-padding the recording with zeros")
        max_size = max([len(layer.data) for layer in self.layers] + [len(self.phrase.data)])
        # postpend zeros to bring all layers to same length
        postpend_length = len(self.phrase.data) - len(self.overdub.data)
        self.overdub.post_padding(postpend_length * [np.zeros(self.number_of_channels * self.frames_per_buffer)])
        self.layers.append(self.overdub.slice(max_size))
        self.overdub = Queue()
        print("Closed recording")

    def extend_recording(self):
        self.phrase.extend_loop()
        print("extended phrase looping")
        for layer in self.layers:
            print("extended layer looping")
            layer.extend_loop()

    def set_overdubbing_mode(self):
        # set to overdubbing if phrase is not empty else set to first recording
        self.is_overdubbing = ~self.phrase.empty()

    def get_rhythm_phrase(self, file_name, genre):
        mid = MidiFile(file_name)
        midi_temp = "temp.mid"
        wav_temp = "temp.wav"
        print("loading sound font from %s" % file_name.split(genre)[0] + genre + '/' + genre + '.sf2')
        fs = FluidSynth(file_name.split(genre)[0] + genre + '/' + genre + '.sf2', sample_rate=self.sample_rate)
        midi_original_tempo = 1000000 * 60 / (mid.tracks[0][5].tempo)
        target_tempo = self.tempo
        for note in mid.tracks[0]:
            note.time = int(note.time * midi_original_tempo / target_tempo)
        mid.save(midi_temp)
        fs.midi_to_audio(midi_temp, wav_temp)
        # os.system("fluidsynth -ni %s %s -F %s -r %s" %(file_name.split(genre)[0] + genre + '/' + genre + '.sf2',midi_temp,wav_temp,self.sample_rate))
        sr, loop_data = wavfile.read(wav_temp)
        # loop_data = np.memmap(wav_temp, np.float32, offset=40)
        print(loop_data.shape)
        loop_data = (loop_data[:len(np.array(self.layers[0].data).flatten())])[::2].reshape(-1, self.frames_per_buffer)
        print(loop_data.shape)
        rhythm_data = list(loop_data)
        rhythm_layer = Queue()
        rhythm_layer.data = rhythm_data
        return rhythm_layer


def peak_detect(data):
    max_val = numpy.amax(abs(data))
    peak_ndx = numpy.where(data == max_val)
    if len(peak_ndx[0]) == 0:  # if nothing found then the max must be negative
        peak_ndx = numpy.where(data == -max_val)
    return peak_ndx


def bpm_detector(data, fs):
    cA = []
    cD = []
    correl = []
    cD_sum = []
    levels = 4
    max_decimation = 2 ** (levels - 1)
    min_ndx = int(60. / 220 * (fs / max_decimation))
    max_ndx = int(60. / 40 * (fs / max_decimation))

    for loop in range(0, levels):
        cD = []
        # 1) DWT
        if loop == 0:
            [cA, cD] = pywt.dwt(data, 'db4')
            cD_minlen = len(cD) // max_decimation + 1
            cD_sum = numpy.zeros(cD_minlen)
        else:
            [cA, cD] = pywt.dwt(cA, 'db4')
        # 2) Filter
        cD = signal.lfilter([0.01], [1 - 0.99], cD)

        # 4) Subtractargs.filename out the mean.

        # 5) Decimate for reconstruction later.
        cD = abs(cD[::(2 ** (levels - loop - 1))])
        cD = cD - numpy.mean(cD)
        # 6) Recombine the signal before ACF
        #    essentially, each level I concatenate
        #    the detail coefs (i.e. the HPF values)
        #    to the beginning of the array
        cD_sum = cD[0:cD_minlen] + cD_sum

    if [b for b in cA if b != 0.0] == []:
        return None, None
    # adding in the approximate data as well...
    cA = signal.lfilter([0.01], [1 - 0.99], cA)
    cA = abs(cA)
    cA = cA - numpy.mean(cA)
    cD_sum = cA[0:cD_minlen] + cD_sum

    # ACF
    correl = numpy.correlate(cD_sum, cD_sum, 'full')

    midpoint = len(correl) // 2
    correl_midpoint_tmp = correl[midpoint:]
    peak_ndx = peak_detect(correl_midpoint_tmp[min_ndx:max_ndx])
    if len(peak_ndx) > 1:
        return None, None

    peak_ndx_adjusted = peak_ndx[0] + min_ndx
    bpm = 60.0 / peak_ndx_adjusted * (fs / max_decimation)
    return bpm[0], correl
