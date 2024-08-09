import numpy as np

class ChordGenerator:

    ROOTSHIFT = {'C':0, 'Db':1, 'D':2, 'Eb':3, 'E':4, 'F':5, 
                'Gb':6, 'G':7, 'Ab':8, 'A':9,'Bb':10, 'B':11}
              
    SCALES = {'major': [0, 2, 4, 5, 7, 9, 11], 'minor': [0, 2, 3, 5, 7, 8, 10]}

    ROMAN2DEGREE = {'i':1, 'ii':2, 'iii':3, 'iv':4, 'v':5, 'vi':6, 'vii':7}

    OCTAVE_C = [12, 24, 36, 48, 60, 72, 84, 96, 108]
    MIDDLE_C = OCTAVE_C[4]

    def __init__(self, purity_ratio:float=0.8):
        self.purity_ratio = purity_ratio
        self.generate_transition_matrix()

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
    
    def generate_transition_matrix(self):
        states = list(self.ROMAN2DEGREE.keys()) + [k.upper() for k in self.ROMAN2DEGREE.keys()]
        self.M_transition_matrix = {}
        self.m_transition_matrix = {}
        M_pref = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii', 'iv', 'VI']
        m_pref = []
        for cur in states:
            self.M_transition_matrix[cur] = {}
            self.m_transition_matrix[cur] = {}
            for next in states:
                if next in M_pref:
                    p = self.purity_ratio/len(M_pref)
                else:
                    p = (1-self.purity_ratio)/(len(states)-len(M_pref))
                self.M_transition_matrix[cur][next] = p
                self.m_transition_matrix[cur][next] = 0.0
        
    def get_next_chord(self, chord):
        p = np.random.random()
        total = 0
        for next_chord, prob in self.M_transition_matrix[chord].items():
            total += prob
            if p < total: break
        return next_chord
# Cmaj 
# I ii iii IV V vi viiº
# Cmin
# i iiº III iv v VI VII

