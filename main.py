import time
import rtmidi


# https://spotlightkid.github.io/python-rtmidi/

class MidiPlayer:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()
        if available_ports:
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("My virtual output")

    def play_note(self, note_on:list, note_off:list, wait_time:float):
        self.midiout.send_message(note_on)
        time.sleep(wait_time)
        self.midiout.send_message(note_off)

    def destruct(self):
        del self.midiout

def main(mp:MidiPlayer):
    print(mp.midiout.send_message([0xC0, 20]))
    for n in range(0,10):
        vel = 127-n*5
        channel = 0
        note_num = 60
        print(f'velocity: {vel}, channel: {channel}, note: {note_num}')
        note_on = [0x90+channel, note_num, vel]  # channel 1, middle C, velocity 112
        note_off = [0x80+channel, note_num, 0]
        mp.play_note(note_on, note_off, 0.1)
        # time.sleep(0.2)
    # mp.midiout.send_message(note_on)
    # time.sleep(1)
    # mp.midiout.send_message(note_off)
    # note_on = [0x90+channel_offset, 40, vel]  # channel 1, middle C, velocity 112
    # note_off = [0x80+channel_offset, 40, 0]
    # mp.play_note(note_on, note_off, 0.1)
    

if __name__ == '__main__':
    mp = MidiPlayer()
    with mp.midiout:
        time.sleep(1)
        main(mp)
    mp.destruct()