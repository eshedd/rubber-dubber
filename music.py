class MusicGenerator:

    ROOTSHIFT = {'C':0, 'Db':1, 'D':2, 'Eb':3, 'E':4, 'F':5, 
                'Gb':6, 'G':7, 'Ab':8, 'A':9,'Bb':10, 'B':11}
              
    SCALES = {'major': [0, 2, 4, 5, 7, 9, 11], 'minor': [0, 2, 3, 5, 7, 8, 10]}

    ROMAN2DEGREE = {'i':1, 'ii':2, 'iii':3, 'iv':4, 'v':5, 'vi':6, 'vii':7}

    OCTAVE_C = [12, 24, 36, 48, 60, 72, 84, 96, 108]
    MIDDLE_C = OCTAVE_C[4]

    def __init__(self): pass

    def roman2degree(self, roman_numeral:str):
        root_degree = self.ROMAN2DEGREE[roman_numeral.lower()]
        chord_type = 'major' if roman_numeral.isupper() else 'minor'
        return root_degree, chord_type

    def get_chord(self, root_degree, scale, chord_type='major', c_octave=60):
            intervals = {
                'major': [0, 4, 7],
                'minor': [0, 3, 7],
                'diminished': [0, 3, 6]
            }
            notes = [scale[(root_degree) % len(scale)] + interval + c_octave for interval in intervals[chord_type]]
            return notes

    def generate_chords(self, key, progression):
        chords = []
        scale = [note + self.ROOTSHIFT[key[0]] for note in self.SCALES[key[1]]]
        for chord in progression:
            roman_numeral = chord[0]
            octave_c = chord[1] if chord[1] else self.MIDDLE_C
            root_degree, chord_type = self.roman2degree(roman_numeral)
            root_degree -= 1
            chords.append(self.get_chord(root_degree, scale, chord_type, octave_c))
        return chords