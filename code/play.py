#!/usr/bin/env python3
"""Play a sine signal."""
import numpy as np
import sounddevice as sd
from wave import make_sound as make
import time
import pygame

pygame.init()

#camera wide & height depends on screen wide & height
scr_w, scr_h = 640, 480

screen = pygame.display.set_mode( (scr_w,scr_h) )
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

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

        self.close = {"sine":(0, False), "square":(0, False), "triangle":(0, False), "sawtooth":(0, False)}

        self.running = True
    def callback(self, data=[], frames=0, time=0, status=0):
        self.t = (self.start_idx + np.arange(frames)) #/ self.sps
        self.t = self.t.reshape(-1, 1)
        self.waveform = self.Oscillators(0, self.close["sine"][0], self.close["sine"][1]) + self.Oscillators(1, self.close["square"][0], self.close["square"][1]) + self.Oscillators(2, self.close["triangle"][0], self.close["triangle"][1]) + self.Oscillators(3, self.close["sawtooth"][0], self.close["sawtooth"][1])
        data[:] = self.atten * (self.waveform)
        self.start_idx += frames

    def sound(self):
        with sd.OutputStream(channels=1, callback=self.callback, samplerate=self.sps):
            while self.running:
                #sd.sleep(1)
                try:
                    temp = [i for i in input("Enter: ").split(" ")]
                    n = int(temp[1])
                    if(temp[2] == "single"):
                        if(temp[0] == "quiet"):
                            temp = None
                            self.set_wave(  (0,False), (0,False), (0,False), (0,False)  )
                        elif(temp[0] == "sine"):
                            temp = None
                            self.set_wave(  (n,True), (n,False), (n,False), (n,False)  )
                        elif(temp[0] == "squ"):
                            temp = None
                            self.set_wave(  (n,False), (n,True), (n,False), (n,False)  )
                        elif(temp[0] == "tri"):
                            temp = None
                            self.set_wave(  (n,False), (n,False), (n,True), (n,False)  )
                        elif(temp[0] == "saw"):
                            temp = None
                            self.set_wave(  (n,False), (n,False), (n,False), (n,True)  )
                        elif(temp[0] == "stop"):
                            break
                    elif(temp[2] == "combine"):
                        if(temp[0] == "sine"):
                            temp = None
                            self.close["sine"] = (n,True)
                        elif(temp[0] == "squ"):
                            temp = None
                            self.close["square"] = (n,True)
                        elif(temp[0] == "tri"):
                            temp = None
                            self.close["triangle"] = (n,True)
                        elif(temp[0] == "saw"):
                            temp = None
                            self.close["sawtooth"] = (n,True)

                except IndexError:
                    if(temp[0] == "quiet"):
                        temp = None
                        self.set_wave(  (0,False), (0,False), (0,False), (0,False)  )
                        print("quiet")
                    elif(temp[0] == "stop"):
                        break
                except ValueError:
                    print(temp,"ValueError")
    
    def set_wave(self, sine, square, triangle, sawtooth):
        self.close["sine"] = sine
        self.close["square"] = square
        self.close["triangle"] = triangle
        self.close["sawtooth"] = sawtooth

    def play_sound(self, sine, square, triangle, sawtooth):
        self.close["sine"] = sine
        self.close["square"] = square
        self.close["triangle"] = triangle
        self.close["sawtooth"] = sawtooth
        self.sound()

    
if __name__ == "__main__":
    wave = play(sps=44100 , freq_hz=440.00, duration_s=5, atten=0.1)
    wave.play_sound(  (0,False), (0,False), (0,False), (0,False)  )
