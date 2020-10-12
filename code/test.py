import numpy as np
import winsound as win
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
class make_sound:
    def __init__(self, sps=44100 , freq_hz=440.00, duration_s=2.0, atten=1):
        # Samples per second
        self.sps = sps #32000

        # Frequency / pitch
        self.freq_hz = freq_hz #440.0

        # Duration
        self.duration_s = duration_s #5.0

        # Attenuation so the sound is reasonable
        self.atten = atten #0.5

    def fourier(self):
        #temp = [float(i) for i in range(int(self.duration_s) * self.sps)]
        #waveform = np.sin(2 * np.pi * t * self.freq_hz / self.sps)
        #self.waveform_quiet = waveform * self.atten

        t = np.arange(self.duration_s * self.sps)
        N = 100
        k = np.arange(1,N+1)
        C_0 = 1/2
        C_x = np.array((k))
        M = np.pi
        wave = 0

        N_temp = 4
        for C in C_x:
            pass
            #wave += np.sin(( 2*np.pi*(C*27.5)*t/self.sps ))
            #wave += C_0 + (M)*np.sin(( 2*np.pi*(C)*t/self.sps ))/(C)
        # https://pages.mtu.edu/~suits/notefreqs.html using frequency
        # f = 2^(n/12) * 440
        n1 = 12
        n2 = -12
        wave = np.sin(( 2*np.pi*(2**(n1/12)*self.freq_hz)*t/self.sps )) + np.sin(( 2*np.pi*(2**(n2/12)*self.freq_hz)*t/self.sps ))
        self.waveform_quiet = wave * self.atten + 50
        #plt.plot( each_sample_number, self.waveform_quiet )
        plt.plot( t, self.waveform_quiet)
        plt.show()
        
        print(wave)
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

sine_wave = make_sound(atten=0.5)
sine_wave.fourier()
sine_wave.write_waveform("test.wav")
sine_wave.play_sound()

"""
Thank you javidx9 from youtube https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA
Thank you alicia.science from youtube https://www.youtube.com/watch?v=ySltrUtlMwI
"""
