import time
import rtmidi
import threading
from music import MusicGenerator

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

def play(mp: MidiPlayer, channel:int, notes:list, velocity:int):
    for note in notes:
        note_on = [0x90 + channel, note, velocity]
        mp.midiout.send_message(note_on)

def stop(mp: MidiPlayer, channel:int, notes:list):
    for note in notes:
        note_off = [0x80 + channel, note, 0]
        mp.midiout.send_message(note_off)

def play_drum_and_melody(mp: MidiPlayer, drum_notes: list, melody_notes: list, wait_time: float):
    drum_channel = 0
    melody_channel = 1
    velocity = 100

    play(mp, drum_channel, drum_notes, velocity)
    play(mp, melody_channel, melody_notes, velocity)
    time.sleep(wait_time)
    stop(mp, melody_channel, melody_notes)


def main(mp: MidiPlayer, melody_chords:list):
    bpm = 125
    quarter_note_duration = 60/bpm  # quarter note in seconds
    eighth_note_duration = quarter_note_duration/2  # eighth note in seconds

    # Trance drum pattern (Kick, Hi-Hat, Clap, Hi-Hat)
    drum_pattern = [
        [36],  # Kick
        [42],  # Hi-Hat
        [38],  # Clap
        [42]   # Hi-Hat
    ]

    # Melody: B-flat minor, F minor, A-flat major, E-flat major over G
    # melody_chords = [
    #     [70, 74, 77],  # B-flat minor (Bb, Db, F)
    #     [65, 69, 72],  # F minor (F, Ab, C)
    #     [68, 72, 75],  # A-flat major (Ab, C, Eb)
    #     [67, 70, 75]   # E-flat major over G (G, Bb, Eb)
    # ]

    # melody_chords = [[60, 64, 67], [67, 71, 74], [69, 72, 76], [53, 57, 60]]
    drop_note = 46

    while True:
        user_input = mp.user_input
        if user_input == '1' and mp.previous_input == '2':  # beat drop
            # Send a single pulse on channel 3 when switching from '2' to '1'
            note_on = [0x90 + 2, drop_note, 127]
            note_off = [0x80 + 2, drop_note, 0]
            mp.midiout.send_message(note_on)
            time.sleep(1.5)
            mp.midiout.send_message(note_off)

        mp.previous_input = user_input

        for i in range(len(melody_chords)):
            melody_notes = melody_chords[i]
            if user_input == '1':  # normal beat
                # Play drum and melody together for 8 beats
                for j in range(8):
                    drum_notes = drum_pattern[j % len(drum_pattern)]
                    play_drum_and_melody(mp, drum_notes, melody_notes, eighth_note_duration)
            elif user_input == '2':  # suspense beat
                # Hold first melody note and cut drum loop in half
                play_drum_and_melody(mp, drum_pattern[0], [melody_notes[0]], eighth_note_duration / 2)
            else:
                return
if __name__ == '__main__':
    mp = MidiPlayer()
    mg = MusicGenerator()

    key = ('C', 'major')

    progression = [('I', None)]
    for _ in range(4):
        chord = mg.get_next_chord('I')
        progression.append((chord, None))
    print(progression)
    melody_chords = mg.generate_chords(key, progression)

    input_thread = threading.Thread(target=mp.listen_for_input)
    input_thread.daemon = True
    input_thread.start()
    with mp.midiout:
        time.sleep(1)
        main(mp, melody_chords)
    mp.destruct()
