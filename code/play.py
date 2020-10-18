#!/usr/bin/env python3
"""Play a sine signal."""
import numpy as np
import sounddevice as sd
from wave import make_sound as make
import time

class play(make):
    def __init__(self, sps=44100 , freq_hz=1.00, duration_s=5, atten=0.5):
        # Samples per second
        self.sps = sps #44100 CD format

        # Frequency / pitch
        self.freq_hz = freq_hz #440.0

        # Duration
        self.duration_s = duration_s #5.0

        # Attenuation so the sound is reasonable
        self.atten = atten #0.5

        self.start_idx = 0

        self.close = {"sine":False, "square":False, "triangle":False, "sawtooth":False}

    def callback(self, outdata=[], frames=0, time=0, status=0):
        self.t = (self.start_idx + np.arange(frames)) #/ self.sps
        self.t = self.t.reshape(-1, 1)
        outdata[:] = self.atten * (self.osci(0, 0, self.close["sine"]) + self.osci(1, 0, self.close["square"]) + self.osci(2, 0, self.close["triangle"]) + self.osci(3, 0, self.close["sawtooth"]))
        self.start_idx += frames

    def play_sound(self):
        with sd.OutputStream(channels=1, callback=self.callback,
                                samplerate=self.sps):
            print('#' * 80)
            print('press Return to quit')
            print('#' * 80)
            input()

if __name__ == "__main__":
    wave = play(sps=44100 , freq_hz=440.00, duration_s=5, atten=0.1)
    wave.close["sine"] = False
    wave.close["square"] = True
    wave.close["triangle"] = False
    wave.close["sawtooth"] = True
    wave.play_sound()