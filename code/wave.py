import numpy as np
import winsound as win
import sounddevice as sd
import argparse
import time
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import math
start_idx = 0

class make_sound:
    def __init__(self, sps=44100 , freq_hz=442.00, duration_s=5, atten=0.1):
        # Samples per second
        self.sps = sps #44100 CD format

        # Frequency / pitch
        self.freq_hz = freq_hz #440.0

        # Duration
        self.duration_s = duration_s #5.0

        # Attenuation so the sound is reasonable
        self.atten = atten #0.5

        self.t = np.arange(self.duration_s*self.sps)
        
        self.close_list = []
        """self.parser = argparse.ArgumentParser(add_help=False)
        self.args, self.remaining = self.parser.parse_known_args()
        self.args = self.parser.parse_args(self.remaining)"""

    def crate_wave(self, mode, n):
        #temp = [float(i) for i in range(int(self.duration_s) * self.sps)]
        #waveform = np.sin(2 * np.pi * t * self.freq_hz / self.sps)
        #self.waveform_quiet = waveform * self.atten

        """N = 100
        k = np.arange(1,N+1)
        C_0 = 1/2
        C_x = np.array((k))
        M = np.pi
        wave = 0
        N_temp = 4
        
        for C in C_x:
            pass
            #wave += C_0 + (M)*np.sin(( 2*np.pi*(C)*t/self.sps ))/(C)"""

        # https://pages.mtu.edu/~suits/notefreqs.html using frequency
        # f = 2^(n/12) * 440

        self.waveform = self.atten*(self.Oscillators())

    def Oscillators(self, mode, n, close):
        if(not close):
            return np.array(0)
        if(mode == 0): # sine wave
            return np.sin( 2*np.pi*(2**(n/12)*self.freq_hz)*self.t/self.sps )
        elif(mode == 1): # square wave
            wave_array = []
            for t in self.t:
                wave = np.sin( 2*np.pi*(2**(n/12)*self.freq_hz)*t/self.sps )
                if(wave > 0):
                    wave_array.append(1)
                else:
                    wave_array.append(-1)

            return np.array(wave_array).reshape(-1, 1)
        elif(mode == 2):
            return abs((2**(n/12)*self.freq_hz)*self.t/self.sps %4 - 2)-1
        elif(mode == 3):
            return (-2*self.atten/np.pi)*np.arctan( 1/( np.tan(  self.t*np.pi*self.freq_hz*(2**(n/12))/self.sps  ) ) )
    
    def plot_wave(self, x, y):
        plt.plot(x, y)
        plt.show()

    def write_waveform(self, name):
        self.waveform_integers_16 = np.int16(self.waveform*32767) # each items at most 32767
        write(name, self.sps, self.waveform_integers_16) # you cann't using wave_yourself, and I don't know why.

if __name__ == "__main__":
    wave = make_sound()
    wave.crate_wave()
    wave.plot_wave()



"""
Thank you javidx9 from youtube https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA
Thank you alicia.science from youtube https://www.youtube.com/watch?v=ySltrUtlMwI
"""
