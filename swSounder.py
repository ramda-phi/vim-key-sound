import pyo
import time


# 'SinWaveSounder' class generates sound file with input character(key-code)
class SinWaveSounder:
    def __init__(self, path):
        self.path = path
        self.scale = 2.0 ** (1 / 12.0)
        self.freq = [0] * 28
        for i in range(28):
            self.freq[i] = 220 * (self.scale ** i)
        self.server = pyo.Server(audio='coreaudio')
        # if you don't use mac, 'pyo.Server()'
        self.server.boot()
        self.server.start()

    def sound(self, ccode, sec):
        t = pyo.HarmTable([1, 0, 0, .2, 0, 0, 0, .1, 0, 0, .05])
        #t = pyo.HarmTable([1, 0, .33, 2, 0, .143, 0, .111])
        amp = pyo.Fader(fadein=.01, fadeout=.07, dur=sec, mul=.2).play()
        osc = pyo.Osc(t,
                freq=[self.freq[ccode], self.freq[ccode] + 1],
                mul=amp).out()
        rec = pyo.Record(osc,
                filename=self.path + "/" + self.seed + ".wav",
                fileformat=0,
                sampletype=1)
        clean = pyo.Clean_objects(sec, rec)
        clean.start()
        time.sleep(sec)

    def random_sound(self, seed, sec):
        self.seed = seed
        ccode = (ord(seed) + 15) % len(self.freq)
        self.sound(ccode, sec)
