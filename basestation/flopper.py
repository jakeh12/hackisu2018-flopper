from header_chunk import HeaderChunk
from track_chunk import TrackChunk
from helpers import HexArrayToDecimal

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

    for track_chunk in track_chunks:
        print(track_chunk.length)
        #print(track_chunk.data.delta_time)
        #print(track_chunk.data.event)
        print([hex(ord(x)) for x in track_chunk.data.raw_data])
