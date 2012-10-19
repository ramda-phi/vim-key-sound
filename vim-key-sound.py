import os
import sys
import time
import swSounder


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


sec = .1
filename = path + "/" + sys.argv[1] + ".wav"
#print '[' + sys.argv[1] + ']'
#print ord(sys.argv[1])

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
    p.terminate()

# if there are no sound source, create sound source
else:
    sounder = swSounder.SinWaveSounder(path)
    sounder.random_sound(sys.argv[1], sec)
    sounder.server.stop()
    time.sleep(.25)
    sounder.server.shutdown()
