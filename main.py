import time
import rtmidi
import threading

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

    def play_note(self, note_on: list, note_off: list, wait_time: float):
        self.midiout.send_message(note_on)
        time.sleep(wait_time)
        self.midiout.send_message(note_off)

    def destruct(self):
        del self.midiout

    def listen_for_input(self):
        while True:
            self.user_input = input("Enter 1 to play as normal, 2 to hold first melody note and cut drum loop in half: ")

def play_drum_and_melody(mp: MidiPlayer, drum_notes: list, melody_notes: list, wait_time: float):
    drum_channel = 0  # Channel 1 for drum
    melody_channel = 1  # Channel 2 for pitched instrument
    velocity = 100

    # Play drum notes
    for note in drum_notes:
        note_on = [0x90 + drum_channel, note, velocity]
        mp.midiout.send_message(note_on)
        note_off = [0x80 + drum_channel, note, 0]
        mp.midiout.send_message(note_off)

    # Play melody notes
    for note in melody_notes:
        note_on = [0x90 + melody_channel, note, velocity]
        mp.midiout.send_message(note_on)

    time.sleep(wait_time)

    # Turn off melody notes
    for note in melody_notes:
        note_off = [0x80 + melody_channel, note, 0]
        mp.midiout.send_message(note_off)

def main(mp: MidiPlayer):
    # Tempo: 122 BPM -> 0.4918 seconds per beat
    bpm = 122
    beat_duration = 30 / bpm

    # Trance drum pattern (Kick, Hi-Hat, Clap, Hi-Hat)
    drum_pattern = [
        [36],  # Kick
        [42],  # Hi-Hat
        [38],  # Clap
        [42]   # Hi-Hat
    ]

    # Melody: B-flat minor, F minor, A-flat major, E-flat major over G
    melody_chords = [
        [70, 74, 77],  # B-flat minor (Bb, Db, F)
        [65, 69, 72],  # F minor (F, Ab, C)
        [68, 72, 75],  # A-flat major (Ab, C, Eb)
        [67, 70, 75]   # E-flat major over G (G, Bb, Eb)
    ]

    # Main notes for each chord
    drop_note = 46

    while True:
        user_input = mp.user_input
        if user_input == '1' and mp.previous_input == '2':
            # Send a single pulse on channel 3 when switching from '2' to '1'
            note_on = [0x90 + 2, drop_note, 127]
            note_off = [0x80 + 2, drop_note, 0]
            mp.midiout.send_message(note_on)
            time.sleep(5)
            mp.midiout.send_message(note_off)

        mp.previous_input = user_input

        for i in range(len(melody_chords)):
            melody_notes = melody_chords[i]
            if user_input == '1':
                # Play drum and melody together for 8 beats
                for j in range(8):
                    drum_notes = drum_pattern[j % len(drum_pattern)]
                    play_drum_and_melody(mp, drum_notes, melody_notes, beat_duration)
            elif user_input == '2':
                # Hold first melody note and cut drum loop in half
                play_drum_and_melody(mp, drum_pattern[0], [melody_notes[0]], beat_duration / 2)

if __name__ == '__main__':
    mp = MidiPlayer()
    input_thread = threading.Thread(target=mp.listen_for_input)
    input_thread.daemon = True
    input_thread.start()
    with mp.midiout:
        time.sleep(1)
        main(mp)
    mp.destruct()
