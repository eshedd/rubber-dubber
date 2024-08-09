import time
import rtmidi
import threading
from music import ChordGenerator

class MidiPlayer:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()
        if available_ports:
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("My virtual output")
        self.user_input = '1'
        self.previous_input = '1'

    def destruct(self):
        del self.midiout

    def listen_for_input(self):
        while True:
            self.user_input = input("Enter 1 to play as normal, 2 to hold first melody note and cut drum loop in half: ")

    def play(self, channel:int, notes:list, velocity:int):
        for note in notes:
            note_on = [0x90 + channel, note, velocity]
            self.midiout.send_message(note_on)

    def stop(self, channel:int, notes:list):
        for note in notes:
            note_off = [0x80 + channel, note, 0]
            self.midiout.send_message(note_off)

class Song:
    def __init__(self, mp:MidiPlayer, bpm:int, drop_note:int, bpc:int=8, standard_velocity:int=100):
        self.mp = mp
        self.bpm = bpm
        self.bpc = bpc  # beats per chord (harmonic rhythm)
        self.standard_velocity = standard_velocity
        self.quarter_note_duration = 60/bpm  # quarter note in seconds
        self.eighth_note_duration = self.quarter_note_duration/2
        self.drop_note = drop_note

    def set_drum(self, drum_channel:int, drum_pattern:list):
        self.drum_channel = drum_channel
        self.drum_pattern = drum_pattern

    def set_melody(self, channel:int, chords:list):
        self.melody_channel = channel
        self.chords = chords
    
    def _drop_beat(self):
        note_on = [0x90 + 2, self.drop_note, 127]
        note_off = [0x80 + 2, self.drop_note, 0]
        self.mp.midiout.send_message(note_on)
        time.sleep(1.5)
        self.mp.midiout.send_message(note_off)
    
    def _standard_bar(self):
        for chord in self.chords:
            melody_notes = chord
            for beat in range(self.bpc):
                drum_notes = self.drum_pattern[beat % len(self.drum_pattern)]
                self._play_drum_and_melody(drum_notes, melody_notes, self.eighth_note_duration)
    
    def _suspense_bar(self):
        for chord in self.chords:
            melody_notes = chord
            self._play_drum_and_melody(self.drum_pattern[0], [melody_notes[0]], self.eighth_note_duration/2)

    def _generating_bar(self):
        pass

    def _play_drum_and_melody(self, drum_notes: list, melody_notes: list, wait_time: float):
        mp.play(self.drum_channel, drum_notes, self.standard_velocity)
        mp.play(self.melody_channel, melody_notes, self.standard_velocity)
        time.sleep(wait_time)
        mp.stop(self.melody_channel, melody_notes)

    def play(self, repeats:int=100):
        for _ in range(repeats):
            if self.mp.user_input == '1':
                self._standard_bar()
            elif self.mp.user_input == '2':
                self._suspense_bar()
            else:
                return
            if self.mp.user_input == '1' and self.mp.previous_input == '2':
                self._drop_beat()
            self.mp.previous_input = self.mp.user_input
        
    def gplay(self, key:tuple=('C', 'major'), steps:int=100):
        cg = ChordGenerator(purity_ratio=0.95)
        self.melody_channel = 1
        chord = ('I', None)
        for _ in range(steps):
            if self.mp.user_input != '1':
                return
            chord = cg.get_next_chord(chord[0])
            melody_notes = cg.generate_chords(key, [(chord, None)])[0]
            for beat in range(self.bpc):
                drum_notes = self.drum_pattern[beat % len(self.drum_pattern)]
                self._play_drum_and_melody(drum_notes, melody_notes, self.eighth_note_duration)


def main(mp: MidiPlayer, endless_generation=False):
    # Trance drum pattern (Kick, Hi-Hat, Clap, Hi-Hat)
    drum_pattern = [
        [36],  # Kick
        [42],  # Hi-Hat
        [38],  # Clap
        [42]   # Hi-Hat
    ]

    cg = ChordGenerator()
    key = ('Bb', 'minor')
    progression = [('I', None)]
    for _ in range(3):
        chord = cg.get_next_chord(progression[-1][0])
        progression.append((chord, None))
    melody_chords = cg.generate_chords(key, progression)
    
    song = Song(mp, bpm=180, drop_note=40, bpc=8)
    song.set_drum(0, drum_pattern)
    song.set_melody(1, melody_chords)

    if endless_generation:
        print('continuously generating chords...')
        song.gplay()
    else:
        print(progression)
        song.play()
    
    
    
if __name__ == '__main__':
    mp = MidiPlayer()
    input_thread = threading.Thread(target=mp.listen_for_input)
    input_thread.daemon = True
    input_thread.start()
    with mp.midiout:
        time.sleep(2)
        main(mp, endless_generation=False)
    mp.destruct()