import midi
import serial
import time

conn = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
midi_pattern = midi.read_midifile("pirates.mid")
ticks_per_qn = midi_pattern.resolution
song_tempo = 500000
all_events = list()

for i, track in enumerate(midi_pattern):
    abs_tick = 0

    for event in track:
        abs_tick += event.tick

        if event.name == 'Set Tempo' or event.name == 'Note On' or event.name == 'Note Off':
            event.track = i + 1
            event.abs_tick = abs_tick
            all_events.append(event)
        '''
        elif event.name == 'Note On':
            note = event.pitch - 24
            channel = event.channel
            delta_time = event.tick
            print("Note On: " + str(note) + " @ Channel " + str(channel) + " -> " + str(delta_time))

            #conn.write([note, (1 << 7) | channel])
            #for i in range(0, 10):
            #    conn.write([note, (1 << 7) | i])

            sleep_time = ((float(delta_time) / ticks_per_qn) * song_tempo) / float(1000000)
            print("Sleeping: " + str(sleep_time))
            time.sleep(sleep_time)
        elif event.name == 'Note Off':
            note = event.pitch - 24
            channel = event.channel
            delta_time = event.tick
            print("Note On: " + str(note) + " @ Channel " + str(channel) + " -> " + str(delta_time))

            #conn.write([note, (channel & 0x7F)])
            #for i in range(0, 10):
            #    conn.write([note, (i & 0x7F)])


            sleep_time = ((float(delta_time) / ticks_per_qn) * song_tempo) / float(1000000)
            print("Sleeping: " + str(sleep_time))
            time.sleep(sleep_time)
        '''

# Sort all the incoming events by their occurring times
all_events.sort(key=lambda x: x.abs_tick)
curr_tick = 0
startTime = time.time()

for event in all_events:
    if event.name == 'Set Tempo':
        song_tempo = event.mpqn
        print("Tempo - " + str(event.abs_tick))
    elif event.name == 'Note On':
        altered_pitch = event.pitch - 24
        delta_time = event.abs_tick - curr_tick

        if delta_time > 0:
            sleep_time = ((float(delta_time) / ticks_per_qn) * song_tempo) / float(1000000)
            print("Sleeping: " + str(sleep_time))
            time.sleep(sleep_time)
            curr_tick += delta_time

        print("Note On: " + str(altered_pitch) + " @ Channel " + str(event.channel) + ", Track " + str(event.track) + " -> " + str(event.abs_tick))

        if event.track == 4:
            for i in range(4, 10):
                conn.write([altered_pitch - ((i % 2) * 12), (1 << 7) | i])
        elif event.track == 3:
            for i in range(2, 4):
                conn.write([altered_pitch, (1 << 7) | i])
        elif event.track == 2:
            for i in range(0, 2):
                conn.write([altered_pitch - ((i % 2) * 12), (1 << 7) | i])

        #conn.write([altered_pitch, (1 << 7) | event.track])

    elif event.name == 'Note Off':
        altered_pitch = event.pitch - 24
        delta_time = event.abs_tick - curr_tick

        if delta_time > 0:
            sleep_time = ((float(delta_time) / ticks_per_qn) * song_tempo) / float(1000000)

            print("Sleeping: " + str(sleep_time))
            time.sleep(sleep_time)
            curr_tick += delta_time

        print("Note Off: " + str(altered_pitch) + " @ Channel " + str(event.channel) + ", Track " + str(event.track) + " -> " + str(event.abs_tick))

        if event.track == 4:
            for i in range(4, 10):
                conn.write([altered_pitch - ((i % 2) * 12), (i & 0x7F)])
        elif event.track == 3:
            for i in range(2, 4):
                conn.write([altered_pitch, (i & 0x7F)])
        elif event.track == 2:
            for i in range(0, 2):
                conn.write([altered_pitch - ((i % 2) * 12), (i & 0x7F)])

        #conn.write([altered_pitch, (event.track & 0x7F)])

endTime = time.time()
print(endTime - startTime)

for i in range(0, 10):
    conn.write([0, (0x7F & i)])

conn.close()
