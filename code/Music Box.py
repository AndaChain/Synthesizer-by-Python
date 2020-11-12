"""Play a signal."""
import numpy as np
import sounddevice as sd
from wave import make_sound as make
from tkinter import*
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
root = Tk()
root.title("Music Box")
root.geometry('1352x700+0+0')
root.configure(background = 'white')

ABC =Frame(root, bg="powder blue", bd=20, relief= RIDGE)
ABC.grid()

ABC1 =Frame(ABC, bg="powder blue", bd=20, relief= RIDGE)
ABC1.grid()
ABC2 =Frame(ABC, bg="powder blue", bd=20, relief= RIDGE)
ABC2.grid()
ABC3 =Frame(ABC, bg="powder blue", bd=20, relief= RIDGE)
ABC3.grid()

class play(make):
    def __init__(self, sps=44100 , freq_hz=440.00, duration_s=5, atten=1):
        super().__init__(sps=44100 , freq_hz=440.00, duration_s=5, atten=1)

        # Samples per second
        self.sps = sps #44100 CD format

        # Frequency / pitch
        self.freq_hz = freq_hz #440.0

        # Duration
        self.duration_s = duration_s #5.0

        # Attenuation so the sound is reasonable
        self.atten = atten #0.5

        self.start_idx = 0
        
        self.signal_mode = {"sin":0, "squ":1, "tri":2, "saw":3}
        self.note = {"B":2, "Bb":1, "A":0, "G#":-1, "G":-2, "F#":-3, "F":-4, "E":-5, "D#":-6, "D":-7, "C#":-8, "C":-9}
        self.keyboard = {"a":[0, -9, False], "s":[0, -8, False],
                        "d":[0, -7, False], "f":[0, -6, False],
                        "g":[0, -5, False], "h":[0, -4, False],
                        "j":[0, -3, False], "k":[0, -3, False],
                        "l":[0, -3, False], ";":[0, -3, False],
                        "QU":[0, -3, False], "BSL":[0, -3, False]}
        self.key_array = ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "QU", "BSL"]
        self.N = 0
        self.waveform = 0
        self.WAVE = "sin"
        self.array_rec = []

    # this is using for play sound continue
    def callback(self, data=[], frames=0, time=0, status=0):
        print(self.start_idx + np.arange(frames))
        self.t = (self.start_idx + np.arange(frames)) #/ self.sps
        self.t = self.t.reshape(-1, 1)
        self.waveform = 0
        self.waveform = np.ones((1136, 1), dtype=float)
        for i in self.key_array:
            for j in range(self.N):
                self.waveform += self.Oscillators(self.keyboard[i][0], self.keyboard[i][1], self.keyboard[i][2])

        data[:] = self.atten * (self.waveform)
        self.start_idx += frames

        temp = np.int16(self.waveform*3000)
        self.array_rec.append(temp)

    # this is for record sound wave to .wav file and show graph sound what you play
    def record(self):
        # record sound
        rec = np.concatenate(self.array_rec)
        write("test.wav", self.sps, rec)

        # graph
        nu = len(rec)
        Time = np.arange(nu)
        plt.xlim(1000,nu,1000*nu)
        plt.ylim(1000,nu,1000*nu)
        plt.plot(Time, rec)
        plt.show()

    # this method for run whatever you want runing parallel with runing sound
    def play_sound(self):
        with sd.OutputStream(channels=1, callback=self.callback, samplerate=self.sps):
            sd.sleep(1)
            def sin_wave() :
                btnCs["state"] = "disable"
                btnCsq["state"] = "normal"
                btnCt["state"] = "normal"
                btnCsaw["state"] = "normal"
                self.WAVE = "sin"
            def square_wave() :
                btnCs["state"] = "normal"
                btnCsq["state"] = "disable"
                btnCt["state"] = "normal"
                btnCsaw["state"] = "normal"
                self.WAVE = "squ"
            def triangle_wave() :
                btnCs["state"] = "normal"
                btnCsq["state"] = "normal"
                btnCt["state"] = "disable"
                btnCsaw["state"] = "normal"
                self.WAVE = "tri"
            def saw_wave() :
                btnCs["state"] = "normal"
                btnCsq["state"] = "normal"
                btnCt["state"] = "normal"
                btnCsaw["state"] = "disable"
                self.WAVE = "saw"
            def style_1() :
                btnCst1["state"] = "disable"
                btnCst2["state"] = "normal"
                btnCst3["state"] = "normal"
                btnCst4["state"] = "normal"
                self.N = 1
            def style_2() :
                btnCst1["state"] = "normal"
                btnCst2["state"] = "disable"
                btnCst3["state"] = "normal"
                btnCst4["state"] = "normal"
                self.N = 2
            def style_3() :
                btnCst1["state"] = "normal"
                btnCst2["state"] = "normal"
                btnCst3["state"] = "disable"
                btnCst4["state"] = "normal"
                self.N = 3
            def style_4() :
                btnCst1["state"] = "normal"
                btnCst2["state"] = "normal"
                btnCst3["state"] = "normal"
                btnCst4["state"] = "disable"
                self.N = 4
            #============================Label with title =====================
            Label(ABC1, text="Synthesizer",font=('arial',25,'bold'),padx=8,pady=8,bd=4,bg="powder blue",
            fg="white").grid(row=0,column=0,columnspan=11)

            #==================================================================

            btnCs=Button(ABC1, height=2, width=6,bd=4, text="sin", font=('arial',18,'bold'),bg="black",fg="white",command = sin_wave)
            btnCs.grid(row=1,column=4,padx=5,pady=5)

            btnCsq=Button(ABC1, height=2, width=6,bd=4, text="square", font=('arial',18,'bold'),bg="black",fg="white",command = square_wave)
            btnCsq.grid(row=1,column=5,padx=5,pady=5)

            btnCt=Button(ABC1, height=2, width=6,bd=4, text="Triangle", font=('arial',18,'bold'),bg="black",fg="white",command = triangle_wave)
            btnCt.grid(row=1,column=6,padx=5,pady=5)

            btnCsaw=Button(ABC1, height=2, width=7,bd=4, text="sawtooth", font=('arial',18,'bold'),bg="black",fg="white",command = saw_wave)
            btnCsaw.grid(row=1,column=7,padx=5,pady=5)

            btnCst1=Button(ABC1, height=2, width=4,bd=4, text="Style1", font=('arial',18,'bold'),bg="black",fg="white",command = style_1)
            btnCst1.grid(row=2,column=4,padx=5,pady=5)

            btnCst2=Button(ABC1, height=2, width=4,bd=4, text="Style2", font=('arial',18,'bold'),bg="black",fg="white",command = style_2)
            btnCst2.grid(row=2,column=5,padx=5,pady=5)

            btnCst3=Button(ABC1, height=2, width=4,bd=4, text="Style3", font=('arial',18,'bold'),bg="black",fg="white",command = style_3)
            btnCst3.grid(row=2,column=6,padx=5,pady=5)

            btnCst4=Button(ABC1, height=2, width=4,bd=4, text="Style4", font=('arial',18,'bold'),bg="black",fg="white",command = style_4)
            btnCst4.grid(row=2,column=7,padx=5,pady=5)

            #==============================Black Button===============================
            btnC_=Button(ABC3, height=4, width=6,bd=4, text="C#", font=('arial',18,'bold'),bg="black",fg="white")
            btnC_.grid(row=0,column=1,padx=5,pady=5)

            btnDs=Button(ABC3, height=4, width=6,bd=4 , text="D#", font=('arial',18,'bold'),bg="black",fg="white")
            btnDs.grid(row=0,column=2,padx=5,pady=5)
            btnSpace=Button(ABC3, state=DISABLED, width=2,height=6 ,bg = "powder blue",relief=FLAT)
            btnSpace.grid(row=0,column=3,padx=0,pady=0)
            btnFs=Button(ABC3, height=4, width=6,bd=4 , text="F#", font=('arial',18,'bold'),bg="black",fg="white")
            btnFs.grid(row=0,column=4,padx=5,pady=5)

            btnGs=Button(ABC3, height=4, width=6,bd=4 , text="G#", font=('arial',18,'bold'),bg="black",fg="white")
            btnGs.grid(row=0,column=5,padx=5,pady=5)
            btnBb=Button(ABC3, height=4, width=6,bd=4 , text="Bb", font=('arial',18,'bold'),bg="black",fg="white")
            btnBb.grid(row=0,column=6,padx=5,pady=5)
            #==================================================================

            #===============================White button==========================
            btnC=Button(ABC3, height=4, width=8, text="C", font=('arial',18,'bold'),bg="white",fg="black")
            btnC.grid(row=1,column=0,padx=5,pady=5)
            btnD=Button(ABC3, height=4, width=8, text="D", font=('arial',18,'bold'),bg="white",fg="black")
            btnD.grid(row=1,column=1,padx=5,pady=5)
            btnE=Button(ABC3, height=4, width=8, text="E", font=('arial',18,'bold'),bg="white",fg="black")
            btnE.grid(row=1,column=2,padx=5,pady=5)
            btnF=Button(ABC3, height=4, width=8, text="F", font=('arial',18,'bold'),bg="white",fg="black")
            btnF.grid(row=1,column=3,padx=5,pady=5)

            btnG=Button(ABC3, height=4, width=8, text="G", font=('arial',18,'bold'),bg="white",fg="black")
            btnG.grid(row=1,column=4,padx=5,pady=5)
            btnA=Button(ABC3, height=4, width=8, text="A", font=('arial',18,'bold'),bg="white",fg="black")
            btnA.grid(row=1,column=5,padx=5,pady=5)
            btnB=Button(ABC3, height=4, width=8, text="B", font=('arial',18,'bold'),bg="white",fg="black")
            btnB.grid(row=1,column=6,padx=5,pady=5)

            root.bind("<a>", wave_obj.KEY_A)
            root.bind("<s>", wave_obj.KEY_S)
            root.bind("<d>", wave_obj.KEY_D)
            root.bind("<f>", wave_obj.KEY_F)
            root.bind("<g>", wave_obj.KEY_G)
            root.bind("<h>", wave_obj.KEY_H)
            root.bind("<j>", wave_obj.KEY_J)
            root.bind("<k>", wave_obj.KEY_K)
            root.bind("<l>", wave_obj.KEY_L)
            root.bind("<;>", wave_obj.KEY_Semi)
            root.bind("<'>", wave_obj.KEY_QU)
            root.bind("</>", wave_obj.KEY_BSL)
            root.bind("<KeyRelease>", wave_obj.KEY_UP)
            #==================================================================
            root.mainloop()

    def KEY_A(self, event):
        self.keyboard["a"] = [self.signal_mode[self.WAVE], self.note["C"], True]

    def KEY_S(self, event):
        self.keyboard["s"] = [self.signal_mode[self.WAVE], self.note["C#"], True]

    def KEY_D(self, event):
        self.keyboard["d"] = [self.signal_mode[self.WAVE], self.note["D"], True]

    def KEY_F(self, event):
        self.keyboard["f"] = [self.signal_mode[self.WAVE], self.note["D#"], True]

    def KEY_G(self, event):
        self.keyboard["g"] = [self.signal_mode[self.WAVE], self.note["E"], True]

    def KEY_H(self, event):
        self.keyboard["h"] = [self.signal_mode[self.WAVE], self.note["F"], True]

    def KEY_J(self, event):
        self.keyboard["j"] = [self.signal_mode[self.WAVE], self.note["F#"], True]

    def KEY_K(self, event):
        self.keyboard["k"] = [self.signal_mode[self.WAVE], self.note["G"], True]

    def KEY_L(self, event):
        self.keyboard["l"] = [self.signal_mode[self.WAVE], self.note["G#"], True]

    def KEY_Semi(self, event):
        self.keyboard[";"] = [self.signal_mode[self.WAVE], self.note["A"], True]

    def KEY_QU(self, event):
        self.keyboard["QU"] = [self.signal_mode[self.WAVE], self.note["Bb"], True]

    def KEY_BSL(self, event):
        self.keyboard["BSL"] = [self.signal_mode[self.WAVE], self.note["B"], True]

    def KEY_UP(self, event) :
        if event.char == 'a' :
            self.keyboard["a"] = [self.signal_mode[self.WAVE], self.note["C"], False]

        if event.char == 's' :
            self.keyboard["s"] = [self.signal_mode[self.WAVE], self.note["C#"], False]

        if event.char == 'd' :
            print(event.char)
            self.keyboard["d"] = [self.signal_mode[self.WAVE], self.note["D"], False]
        
        if event.char == 'f' :
            print(event.char)
            self.keyboard["f"] = [self.signal_mode[self.WAVE], self.note["D#"], False]

        if event.char == 'g' :
            print(event.char)
            self.keyboard["g"] = [self.signal_mode[self.WAVE], self.note["E"], False]

        if event.char == 'h' :
            print(event.char)
            self.keyboard["h"] = [self.signal_mode[self.WAVE], self.note["F"], False]

        if event.char == 'j' :
            print(event.char)
            self.keyboard["j"] = [self.signal_mode[self.WAVE], self.note["F#"], False]

        if event.char == 'k' :
            print(event.char)
            self.keyboard["k"] = [self.signal_mode[self.WAVE], self.note["G"], False]

        if event.char == 'l' :
            print(event.char)
            self.keyboard["l"] = [self.signal_mode[self.WAVE], self.note["G#"], False]

        if event.char == ';' :
            print(event.char)
            self.keyboard[";"] = [self.signal_mode[self.WAVE], self.note["A"], False]

        if event.char == "'" :
            print(event.char)
            self.keyboard["QU"] = [self.signal_mode[self.WAVE], self.note["Bb"], False]

        if event.char == '/' :
            print(event.char)
            self.keyboard["BSL"] = [self.signal_mode[self.WAVE], self.note["B"], False]


if __name__ == "__main__":
    wave_obj = play(sps=44100 , freq_hz=440.00, duration_s=5, atten=0.3)
    wave_obj.play_sound()
    wave_obj.record()
