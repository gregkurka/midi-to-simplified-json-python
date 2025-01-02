# midi-to-simplified-json-python
a midi to simplified JSON script I made while working with Kooapps on their game Piano Tiles 2. Requires some editing to the midi via cubase. Also finishing touches come from Kooapps in-house editor.

It is important to note that the only data that matters in their game is length, and note name. Notes cannot overlap, unless they start and stop at the same time. Therefore, we run some functions in cubase to help us simplify the midi file.

# requirements
Before running this script, you use the following functions in Cubase on all notes in the midi file:

1. Simplify tracks down to as few tracks as makes sense.
2.  Quantize appropriately for exact timing
3. Change lengths by setting quantize function to 1/128 dotted, and hit fixed lengths
4. Run legato function on each voice
5. Run "Delete doubles"
6. Run "Delete overlaps (poly)
7. Export new midi file

Run this python script on the new midi file.
Edit in Kooapps Editor


