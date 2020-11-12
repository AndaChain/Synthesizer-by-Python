import numpy as np
import winsound as win
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import matplotlib.animation as animation
start_idx = 0

class make_sound:
    def __init__(self, sps=44100 , freq_hz=440.00, duration_s=5, atten=0.1):
        # Samples per second
        self.sps = sps #44100 CD format

        # Frequency / pitch
        self.freq_hz = freq_hz #440.0

        # Duration
        self.duration_s = duration_s #5.0

        # Attenuation so the sound is reasonable
        self.atten = atten #0.5

        # Time
        self.t = np.arange(self.duration_s*self.sps)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        
    def crate_wave(self, mode, n):
        # https://pages.mtu.edu/~suits/notefreqs.html using frequency
        self.waveform = self.atten*(self.Oscillators(mode, n, True))

    def Oscillators(self, mode, n, status):
        if(not status):
            return 0*np.arange(1136).reshape(-1,1)
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
        elif(mode == 2): # triangle wave
            return abs(  4*((self.freq_hz*self.t*(2**(n/12)))/self.sps)%4  - 2)-1
        elif(mode == 3): # sawtooth wave
            return (-2*self.atten/np.pi)*np.arctan( 1/( np.tan(  self.t*np.pi*self.freq_hz*(2**(n/12))/self.sps  ) ) )        

    def write_waveform(self, name):
        self.waveform_integers_16 = np.int16(self.waveform*32767)
        write(name, self.sps, self.waveform_integers_16)
    
    def plot_wave(self):
        plt.plot(self.t[0:100], self.waveform[0:100])
        plt.show()

if __name__ == "__main__":
    wave = make_sound()
    wave.crate_wave(0, 4)
    wave.plot_wave()
    wave.write_waveform("test.wav")


"""
Thank you javidx9 from youtube https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA
Thank you alicia.science from youtube https://www.youtube.com/watch?v=ySltrUtlMwI
Thank you MajorThird from github https://github.com/MajorThird/continuous-synthesizer
"""
