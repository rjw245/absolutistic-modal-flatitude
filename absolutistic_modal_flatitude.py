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

# Which notes to play for the
# Ionian mode.
ionian = [True,   # 1
          False,  # flat 2
          True,   # 2
          False,  # flat 3
          True,   # 3
          True,   # 4
          False,  # flat 5
          True,   # 5
          False,  # flat 6
          True,   # 6
          False,  # 7 (sometimes called flat 7)
          True]   # major 7 (sometimes just called 7)

# Notes to play for whatever mode we are in.
# Use a deque so that, when the root is displaced
# (i.e. first note of the scale is no longer C5),
# we can rotate the scale back to return the root to C5.
cur_mode = deque(ionian)  # Copy the Ionian mode as the current mode

if __name__ == "__main__":
    while True:
        # Play one scale
        for note_idx in xrange(0, len(frequencies)):
            should_play = cur_mode[note_idx % len(cur_mode)]
            if should_play:
                freq = frequencies.values()[note_idx]
                play_note(freq, 0.3)

        # Find the f-f-h-f-f-f-h pattern (Ionian mode) wherever
        # it is in the current mode
        (start, end) = contains(ionian, cur_mode)

        # Flat the 7th note of the pattern to move us to a new mode
        # of this scale
        temp = cur_mode[(end-2) % len(cur_mode)]
        cur_mode[(end-2) % len(cur_mode)] = cur_mode[(end-1) % len(cur_mode)]
        cur_mode[(end-1) % len(cur_mode)] = temp

        # Make sure C stays the root.
        # If we wrap around modes, shift back to a C scale.
        if not cur_mode[0]:
            cur_mode.rotate(1)

        time.sleep(1)
