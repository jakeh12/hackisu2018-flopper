import midi
import serial
import time

#conn = serial.Serial('')
midi_pattern = midi.read_midifile("happy_birthday.mid")
ticks_per_qn = midi_pattern.resolution
song_tempo = 500000

for track in midi_pattern:
    for event in track:
        if event.name == 'Note On':
            note = event.pitch
            channel = event.channel
            delta_time = event.tick
            print("Note On: " + str(note) + " @ Channel " + str(channel) + " -> " + str(delta_time))
            #conn.write([note, (1 << 7) | channel])
            sleep_time = ((float(delta_time) / ticks_per_qn) * song_tempo) / float(1000000)
            print("Sleeping: " + str(sleep_time))
            time.sleep(sleep_time)
        elif event.name == 'Note Off':
            note = event.pitch
            channel = event.channel
            delta_time = event.tick
            print("Note On: " + str(note) + " @ Channel " + str(channel) + " -> " + str(delta_time))
            #conn.write([note, (0 & 0x7F) | channel])
            sleep_time = ((float(delta_time) / ticks_per_qn) * song_tempo) / float(1000000)
            print("Sleeping: " + str(sleep_time))
            time.sleep(sleep_time)
#conn.close()
