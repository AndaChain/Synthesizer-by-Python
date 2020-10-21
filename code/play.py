#!/usr/bin/env python3
"""Play a signal."""
import numpy as np
import sounddevice as sd
from wave import make_sound as make
import time

class play(make):
    def __init__(self, sps=44100 , freq_hz=1.00, duration_s=5, atten=0.5):
        super().__init__(sps=44100 , freq_hz=1.00, duration_s=5, atten=0.5)

        # Samples per second
        self.sps = sps #44100 CD format

        # Frequency / pitch
        self.freq_hz = freq_hz #440.0

        # Duration
        self.duration_s = duration_s #5.0

        # Attenuation so the sound is reasonable
        self.atten = atten #0.5

        self.start_idx = 0

        self.close = {"sine":[0, 0, False], "square":[1, 0, False], "triangle":[2, 0, False], "sawtooth":[3, 0, False]}

        self.note = {"B":2, "Bb":1, "A":0, "G#":-1, "G":-2, "F#":-3, "F":-4, "E":-5, "D#":-8, "D":-7, "C#":-8, "C":-9}
        self.running = True

        self.combine_wave = []

        self.form = "sine"
        self.N = "A"
        self.num = 1
        self.state = self.close[self.form][2]
        self.waveform = 0

    def callback(self, data=[], frames=0, time=0, status=0):
        
        self.t = (self.start_idx + np.arange(frames)) #/ self.sps
        self.t = self.t.reshape(-1, 1)
        self.waveform = 0

        for i in range(self.num):
            self.waveform += self.Oscillators(  self.close[self.form][0],
                                            self.close[self.form][1]+i*8,
                                            self.close[self.form][2]  )

        data[:] = self.atten * (self.waveform)
        self.start_idx += frames

    def play_sound(self):
        with sd.OutputStream(channels=1, callback=self.callback, samplerate=self.sps):
            while self.running:
                sd.sleep(1)
                try:
                    temp = [i for i in input(f"Enter {self.form} {self.N}:").split(" ")]
                    mode = temp[0]
                    self.N = temp[1]
                    self.num = int(temp[2])
                    print( self.freq_hz*(2**(self.note[self.N]/12)) )

                    if(mode == "sine"):
                        self.form = "sine"
                        self.close[self.form][1] = self.note[self.N]
                        self.close[self.form][2] = True
                    elif(mode == "squ"):
                        self.form = "square"
                        self.close[self.form][1] = self.note[self.N]
                        self.close[self.form][2] = True
                    elif(mode == "tri"):
                        self.form = "triangle"
                        self.close[self.form][1] = self.note[self.N]
                        self.close[self.form][2] = True
                    elif(mode == "saw"):
                        self.form = "sawtooth"
                        self.close[self.form][1] = self.note[self.N]
                        self.close[self.form][2] = True
                    self.state = temp
                    
                except IndexError:
                    if(temp[0] == "||"):
                        self.close[self.form][2] = False
                        print(self.form,5)
                    elif(temp[0] == ">"):
                        self.close[self.form][2] = True
                        print(self.form)
                    elif(mode == "plot"):
                        self.plot_wave()
                    elif(temp[0] == 'X'):
                        self.close[self.form][2] = False
                        break
                    print(temp[0],"IndexError")
                except KeyError:
                    print(self.state)
                    
if __name__ == "__main__":
    wave_obj = play(sps=44100 , freq_hz=440.00, duration_s=5, atten=1)
    wave_obj.play_sound()
