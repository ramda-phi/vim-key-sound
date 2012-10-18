# coding: utf-8

#"========================================================================="
#
#   vim-key-sound.py
#
#   'vim-key-sound.py' is forked from 
#
#   ✘╹◡╹✘  音の鳴るエディタことVim
#   http://r7kamura.hatenablog.com/entry/2012/10/09/155041
#
#   ssig33.com 音が鳴るエディタ軽量化
#   http://ssig33.com/text/音が鳴るエディタ軽量化
#
#   [Requirements]
#    to use 'vim-key-sound.py', you need
#
#       portaudio
#       pyaudio
#       pyo
#       vimproc
#
#    Sorry, I verified this code only on Mac OS X Lion 10.7.5, python 2.7.3
#
#   [to Use]
#
#    set 'vks/tmp' in your home directory or rewrite variable 'path'
#
#       path = any_dir/you_set
#
#    and add this code in your .vimrc
#
#       autocmd CursorMovedI * :call vimproc#system_bg("python " . path/to/vim-key-sound/vim-key-sound.py " .getline('.')[col('.')-2])
#
#   [Known Bugs & todo]
#
#   1. No exception handling ['] in vimproc
#   2. There are only one sound set. some snd set will be added
#   3. without 'pyo' version
#   4. and more
#
#"========================================================================="

import os
import sys
import time


# please start with soundfile(.wav)
if len(sys.argv) < 2:
    print ('Plays a wave file.\n\nUsage: %s filename.wav' % sys.argv[0])
    sys.exit(-1)

# if there are no sound source dir, create directory to save sound files
path = "vks/tmp"
if os.path.exists(path):
    pass
else:
    os.makedirs(path)


# 'SinWaveSounder' class generates sound file with input character(key-code)
class SinWaveSounder:
    def __init__(self):
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
                filename=path + "/" + sys.argv[1] + ".wav",
                fileformat=0,
                sampletype=1)
        clean = pyo.Clean_objects(sec, rec)
        clean.start()
        time.sleep(sec)

    def random_sound(self, seed, sec):
        ccode = (ord(seed) + 15) % len(self.freq)
        self.sound(ccode, sec)


sec = .1
filename = path + "/" + sys.argv[1] + ".wav"

if os.path.exists(filename):
    import pyaudio
    import wave
    f = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = f.readframes(frame_count)
        return data, pyaudio.paContinue

    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
            channels=f.getnchannels(),
            rate=f.getframerate(),
            output=True,
            stream_callback=callback)
    stream.start_stream()
    while stream.is_active():
        time.sleep(.1)
    stream.stop_stream()
    stream.close()
    f.close()
    p.termionate()

# if there are no sound source, create sound source
else:
    import pyo
    sounder = SinWaveSounder()
    sounder.random_sound(sys.argv[1], sec)
    sounder.server.stop()
    time.sleep(.25)
    sounder.server.shutdown()
