from header_chunk import HeaderChunk
from track_chunk import TrackChunk
from helpers import HexArrayToDecimal, OctaveMatch
from time import sleep

#with open('/home/justin/Documents/pirates.mid', 'rb') as midiFile:
with open('/home/justin/Documents/mario.mid', 'rb') as midiFile:
#with open('/home/justin/Documents/happy_birthday.mid', 'rb') as midiFile:
    # Read entire file and save into a list of ascii/hex chars
    fileContent = list(midiFile.read())

    # Parse the header chunk
    header_chunk = HeaderChunk(HexArrayToDecimal(fileContent[0:14]))

    # Print header chunk
    print("Header:")
    print("Type: " + str(header_chunk.type))
    print("Length: " + str(header_chunk.length))
    print("Format: " + str(header_chunk.data.format))
    print("# Tracks: " + str(header_chunk.data.tracks))
    print("Division Format: " + str(header_chunk.data.division_format))

    if header_chunk.data.division_format == 1:
        print("-frames/second: " + str(header_chunk.data.frames_per_second))
        print("ticks/frame: " + str(header_chunk.data.ticks_per_frame))
    else:
        print("ticks per quarter note: " + str(header_chunk.data.ticks_per_quarter_note))

    # Create the list to hold all the tracks
    track_chunks = list()

    # Pointer to next track starts directly after header chunk (14 bytes)
    pointer = 14

    # Iterate through entire file and capture track chunks
    while len(track_chunks) < header_chunk.data.tracks:
        next_track_size = HexArrayToDecimal(fileContent[(pointer + 4):(pointer + 8)])
        track_chunks.append(TrackChunk(fileContent[pointer:(pointer + next_track_size + 8)]))
        pointer += next_track_size + 8

    print("Track chunks found: " + str(len(track_chunks)))

    song_tempo = 0
    all_notes = list()

    for track_chunk in track_chunks:
        print("Track length: " + str(track_chunk.length))
        print("Hex dump: " + str([hex(ord(x)) for x in track_chunk.data.raw_data]))
        track_notes = track_chunk.data.notes
        print("Notes: " + str(track_notes))

        if len(track_notes) >= 5:
            all_notes += track_notes

        temp_tempo = track_chunk.data.tempo

        if temp_tempo != 0:
            song_tempo = temp_tempo

    print("Tempo (us/qn): " + str(song_tempo))

    # Order notes
    for i in range(len(all_notes) - 1, 0, -1):
        for x in range(i):
            if all_notes[x][1] > all_notes[x + 1][1]:
                temp = all_notes[x]
                all_notes[x] = all_notes[x + 1]
                all_notes[x + 1] = temp

    print("All notes: " + str(all_notes))

    # Information stored in tuple: (available, startTime, note)
    available_drives = [(1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0),
                        (1, 0, 0)]
    current_time = 0

    for note in all_notes:
        if note[1] <= current_time:
            #print(note)

            if note[2] == 1:
                # Need to find first available drive
                for i in range(0, len(available_drives)):
                    if available_drives[i][0] == 1:
                        available_drives[i] = (0, note[1], note[0])
                        print("SENDING: (note = " + str(OctaveMatch(note[0])) + ", drive = " + str(i) + ", on = 1")
                        break
            else:
                for i in range(0, len(available_drives)):
                    if available_drives[i][0] == 0 and available_drives[i][2] == note[0]:
                        available_drives[i] = (1, 0, 0)     # Make drive available
                        print("SENDING: (note = " + str(OctaveMatch(note[0])) + ", drive = " + str(i) + ", on = 0")
                        break
        else:
            delta_time = note[1] - current_time
            sleep_time = ((song_tempo / header_chunk.data.ticks_per_quarter_note) * delta_time) / float(1000000)
            print("Sleeping: " + str(sleep_time))
            sleep(sleep_time)
            current_time += delta_time
            #print(note)

            if note[2] == 1:
                # Need to find first available drive
                for i in range(0, len(available_drives)):
                    if available_drives[i][0] == 1:
                        available_drives[i] = (0, note[1], note[0])
                        print("SENDING: (note = " + str(OctaveMatch(note[0])) + ", drive = " + str(i) + ", on = 1")
                        break
            else:
                for i in range(0, len(available_drives)):
                    if available_drives[i][0] == 0 and available_drives[i][2] == note[0]:
                        available_drives[i] = (1, 0, 0)     # Make drive available
                        print("SENDING: (note = " + str(OctaveMatch(note[0])) + ", drive = " + str(i) + ", on = 0")
                        break

        #print(available_drives)
