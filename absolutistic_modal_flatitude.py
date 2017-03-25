import math
import pyaudio
import time
from collections import OrderedDict, deque
from itertools import cycle

p = pyaudio.PyAudio()


def play_note(freq, duration):
    # See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 16000  # number of frames per second/frameset.

    NUMBEROFFRAMES = int(BITRATE * duration)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''

    for x in xrange(NUMBEROFFRAMES):
        WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/freq)/math.pi))*127+128))    

    # fill remainder of frameset with silence
    for x in xrange(RESTFRAMES):
        WAVEDATA = WAVEDATA+chr(128)

    stream = p.open(format=p.get_format_from_width(1),
                    channels=1,
                    rate=BITRATE,
                    output=True)
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()


def contains(small, big):
    big_cycle = list(big) + list(big)  # Allows us to wrap around the end
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
cur_mode = deque([True,
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


if __name__ == "__main__":
    while True:
        # Play one scale
        for note_idx in xrange(0, len(frequencies)):
            should_play = cur_mode[note_idx % len(cur_mode)]
            if should_play:
                freq = frequencies.values()[note_idx]
                play_note(freq, 0.3)

        # Find the full-full-full-half-step subpattern
        # in the current mode (5 note subpattern)
        subpattern = [False, True,  # Full step (one unplayed, next played)
                      False, True,  # Full step
                      False, True,  # Full step
                      True]         # Half step
        (start, end) = contains(subpattern, cur_mode)

        # Flat the 4th note of the subpattern to move us to a new mode
        # of this scale
        temp = cur_mode[(end-3) % len(cur_mode)]
        cur_mode[(end-3) % len(cur_mode)] = cur_mode[(end-2) % len(cur_mode)]
        cur_mode[(end-2) % len(cur_mode)] = temp

        # Make sure C stays the root. If we wrap around modes, shift
        # back to a C scale.
        if not cur_mode[0]:
            cur_mode.rotate(1)

        time.sleep(1)
