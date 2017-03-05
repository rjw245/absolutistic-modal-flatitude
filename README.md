Requires pyaudio, which depends on portaudio for Linux.

You can install portaudio with dev headers like so:

~~~~
sudo apt-get install portaudio19-dev
~~~~

Cycles through all scales, starting with the C major scale.
I'm pretty proud of this. It has a list of all possible notes
in the C scale, as well as the pattern of which notes to play
and which not to. I exploit absolutistic modal flatitude in that
we always flat the 4th note in any full-full-full-half step pattern
(steps between notes). An example of a full step is from C to D
(skipping C#) and an example of a half step is E to F (no note
inbetween).
I find this full-full-full-half pattern wherever it is in my
larger pattern of the current scale (it may wrap around the edge)
and I flat that particular note, and continue playing.
Once I go over the edge (transition past Locrian) my new root WOULD be
D, but I rotate my pattern back around so that my root continues to be
the lower C note.