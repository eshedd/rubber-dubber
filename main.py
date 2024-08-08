import time
import rtmidi

class MidiPlayer:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()
        if available_ports:
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("My virtual output")

    def play_note(self, note_on: list, note_off: list, wait_time: float):
        self.midiout.send_message(note_on)
        time.sleep(wait_time)
        self.midiout.send_message(note_off)

    def destruct(self):
        del self.midiout

def play_drum_and_melody(mp: MidiPlayer, drum_notes: list, melody_notes: list, main_note: int, wait_time: float):
    drum_channel = 0  # Channel 1 for drum
    melody_channel = 1  # Channel 2 for pitched instrument
    extra_channel = 2  # Channel 3 for extra signals
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
        [36],  # Kick and Hi-Hat
        [42],  # Hi-Hat
        [38],  # Clap and Hi-Hat
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
    main_notes = [70, 65, 68, 67]

    # Loop through the pattern
    for _ in range(8):  # Repeat the pattern 4 times
        for i in range(len(melody_chords)):
            melody_notes = melody_chords[i]
            main_note = main_notes[i]
            # Play drum and melody together for 8 beats (4 seconds)
            for j in range(8):
                drum_notes = drum_pattern[j % len(drum_pattern)]
                play_drum_and_melody(mp, drum_notes, melody_notes, main_note, beat_duration)

if __name__ == '__main__':
    mp = MidiPlayer()
    with mp.midiout:
        time.sleep(1)
        main(mp)
    mp.destruct()
