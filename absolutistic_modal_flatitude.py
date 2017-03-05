import math
import pyaudio
from collections import OrderedDict, deque
from itertools import cycle


def contains(small, big):
    big_cycle = list(big) + list(big)
    for i in xrange(0, len(big)):
        for j in xrange(len(small)):
            if big_cycle[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

frequencies = OrderedDict()
frequencies['C5'] = 523.25
frequencies['C#'] = 554.37
frequencies['D'] = 587.33
frequencies['D#'] = 622.25
frequencies['E'] = 659.25
frequencies['F'] = 698.46
frequencies['F#'] = 739.99
frequencies['G'] = 783.99
frequencies['G#'] = 830.61
frequencies['A'] = 880.0
frequencies['A#'] = 932.33
frequencies['B'] = 987.77
frequencies['C6'] = 1046.50

# Initial values describe
# the notes to play for the Ionian
# mode
to_play = deque([True,
                 False,
                 True,
                 False,
                 True,
                 True,
                 False,
                 True,
                 False,
                 True,
                 False,
                 True])

while True:
    # Play one scale
    for note_idx in xrange(0, len(frequencies)):
        should_play = to_play[note_idx % len(to_play)]
        if should_play:
            # sudo apt-get install python-pyaudio
            PyAudio = pyaudio.PyAudio

            # See http://en.wikipedia.org/wiki/Bit_rate#Audio
            BITRATE = 16000  # number of frames per second/frameset.

            # See http://www.phy.mtu.edu/~suits/notefreqs.html
            FREQUENCY = frequencies.values()[note_idx % len(frequencies)]
            LENGTH = .3  # seconds to play sound

            NUMBEROFFRAMES = int(BITRATE * LENGTH)
            RESTFRAMES = NUMBEROFFRAMES % BITRATE
            WAVEDATA = ''

            for x in xrange(NUMBEROFFRAMES):
                WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    

            # fill remainder of frameset with silence
            for x in xrange(RESTFRAMES):
                WAVEDATA = WAVEDATA+chr(128)

            p = PyAudio()
            stream = p.open(format=p.get_format_from_width(1),
                            channels=1,
                            rate=BITRATE,
                            output=True)
            stream.write(WAVEDATA)
            stream.stop_stream()
            stream.close()
            p.terminate()

    # Find the full-full-full-half-step pattern
    # in the current scale (5 note subpattern)
    pattern = [False, True,  # Full step
               False, True,  # Full step
               False, True,  # Full step
               True]         # Half step
    (start, end) = contains(pattern, to_play)
    temp = to_play[(end-3) % len(to_play)]

    # Flat the 4th note of the subpattern to move us to a new mode
    # of this scale
    to_play[(end-3) % len(to_play)] = to_play[(end-2) % len(to_play)]
    to_play[(end-2) % len(to_play)] = temp

    # Must always play the first note, keep it a C scale
    if not to_play[0]:
        to_play.rotate(1)
