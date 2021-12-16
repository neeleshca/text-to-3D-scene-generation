# text-to-3D-scene-generation<br>
Note: This repository only serves as a reference, and is not meant for reproducible work.

High level codeflow was that the user types a sentence. The sentence is parsed using Stanford CoreNLP. The parsed output is fed into a python script which visualizes the output in blender. The scene we considered was a room, and the objects that could be placed were desks, tables etc. Prepositions were covered, e.g. "table in the center of the room"  would place a table in the middle of the room. For object placement, bounds checking and object collision are handled.
