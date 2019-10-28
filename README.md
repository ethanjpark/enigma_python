# enigma_python

Rotor and reflector wirings to be chosen from rotor wiring tables here:
https://en.wikipedia.org/wiki/Enigma_rotor_details

3-rotor configurations and plugboard configurations from here:
https://en.wikipedia.org/wiki/Enigma_machine#/media/File:Enigma_keylist_3_rotor.jpg

Ring setting (ringstellung) and rotor starting position explained here: (easy to confuse them)
http://users.telenet.be/d.rijmenants/en/enigmatech.htm

Usage:
`python input.py I II III A 1 2 3 A B C 29`

`python input.py 29 A A B C`


### File Breakdown

engima.py - the actual polyalphabetic substitution algorithm used by enigma. Algorithm is called by input.py

input.py - command line input argument processing and calling of the algorithm

plugboard.py - Contains the plugboard pairings for the 29th, 30th, and 31st from keylist #649 from link above

rotors.py - Contains the rotor wiring dictionaries for rotors I, II, III, IV, V and reflectors A, B, C