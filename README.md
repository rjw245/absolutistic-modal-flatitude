I started taking guitar lessons recently, and my teacher [Sam Davis](http://www.samdavis.com/) taught me about modes of the major scale and the relationship between them.

He calls this concept "absolutistic modal flatitude", hence the name of this project. I don't think this is a widely-used term though...

Anyway, the idea is that if you flat a particular note of the C major scale (or any scale I think), it will take you to the next mode of that scale, and each mode will sound darker than the last. The note to flat is one that preserves the full-full-half-full-full-full-half step pattern (steps between notes) somewhere in the scale. An example of a full step is from C to D (skipping C#) and an example of a half step is E to F (no note
inbetween). I wanted to prove that I understood the concept, so I boiled it down to this simple program.

Basically, this program cycles through all modes of the C major scale.
It has a list of all notes in the C chromatic scale, as well as the pattern of which notes to play
and which not to for the Ionian mode (most common).
I exploit absolutistic modal flatitude in that
I always flat the 4th note in any full-full-full-half step pattern
(steps between notes) to move to the next mode.
I find this full-full-full-half pattern wherever it is in my
larger pattern of the current mode (it may wrap around the edge)
and I flat that particular note, and continue playing.
Once I go over the edge (transition past the Locrian mode) my new root WOULD be the D note, but I rotate my pattern back around so that my root continues to be the lower C.

Requires pyaudio, which depends on portaudio for Linux.

You can install portaudio with dev headers like so:

~~~~
sudo apt-get install portaudio19-dev
~~~~
