import numpy as np
from math import pi,sin,cos
import winsound as win
from scipy.io.wavfile import write
import time

class make_sound:
    def __init__(self, sps=32000, freq_hz=440.0, duration_s=2.0, atten=1):
        # Samples per second
        self.sps = sps #32000

        # Frequency / pitch
        self.freq_hz = freq_hz #440.0

        # Duration
        self.duration_s = duration_s #5.0

        # Attenuation so the sound is reasonable
        self.atten = atten #0.5

    def fourier(self):
        each_sample_number = np.arange(self.duration_s * self.sps)
        temp = [float(i) for i in range(int(self.duration_s) * self.sps)]
        waveform = np.sin(2 * np.pi * each_sample_number * self.freq_hz / self.sps)
        self.waveform_quiet = waveform * self.atten

        """
        each_sample_number is time
        self.freq_hz is Frequency of wave
        self.sps is number of sample
        """

        #temp = [float(i) for i in range(int(self.duration_s) * self.sps)]
        #self.waveform_2 = [sin(2 * pi * i * self.freq_hz / self.sps) for i in temp]
        
    def write_waveform(self, name):
        # Write sound to .wav
        #waveform_integers = np.int64(self.waveform_quiet*9.223372*10**18)
        #waveform_integers_32 = np.int32(self.waveform_quiet*2147483647)
        #wave_yourself = [int(i * 32767) for i in self.waveform_2]

        waveform_integers_16 = np.int16(self.waveform_quiet*32767) # each items at most 32767
        write(name, self.sps, waveform_integers_16) # you cann't using wave_yourself, and I don't know why.
        

    def play_sound(self):
        # Play the waveform out the speakers
        win.PlaySound("test.wav",win.SND_FILENAME)

sine_wave = make_sound()
sine_wave.fourier()
sine_wave.write_waveform("test.wav")
sine_wave.play_sound()

"""
Thank you javidx9 from youtube https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA
Thank you alicia.science from youtube https://www.youtube.com/watch?v=ySltrUtlMwI
"""
