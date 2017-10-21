from header_chunk import HeaderChunk

def HexArrayToDecimal(hex_list):
    dec_value = 0
    byte_size = 8
    shift_amount = ((len(hex_list) - 1) * byte_size)

    for hex_byte in hex_list:
        temp_value = ord(hex_byte) << shift_amount
        dec_value = dec_value | temp_value
        shift_amount -= byte_size

    return dec_value

with open('/home/justin/Documents/happy_birthday.mid', 'rb') as midiFile:
    fileContent = list(midiFile.read())
    header_chunk = HeaderChunk(HexArrayToDecimal(fileContent[0:14]))
    print(hex(HexArrayToDecimal(fileContent[0:14])))






    '''
    # Parse header chunk
    # Type (4 bytes) - Length (4 bytes) - Data (2 / 2 / 2 bytes)
    header_type = HexArrayToDecimal(fileContent[0:4])
    header_length = HexArrayToDecimal(fileContent[4:8])
    data_format = HexArrayToDecimal(fileContent[8:10])
    data_tracks = HexArrayToDecimal(fileContent[10:12])
    data_division = HexArrayToDecimal(fileContent[12:14])

    header_chunk = HeaderChunk(header_length, data_format, data_tracks, data_division)

    print("Header Length: " + str(header_length))
    print("Format: " + str(data_format))
    print("# Tracks: " + str(data_tracks))

    # Check to see if bit 15 is 1 or 0
    if ((data_division & 0x8000) >> ((2 * byte_size) - 1)) == 1:
        # Bit 15 == 1
        # Bits 8-14 == -frames/second
        # Bits 0-7 == ticks/frame
        frames_per_second = (data_division & 0xEF00) >> byte_size
        ticks_per_frame = (data_division & 0x00FF)
        print("Frames / Second: " + str(frames_per_second))
        print("Ticks / Second " + str(ticks_per_frame))
    else:
        # Bit 15 == 0
        # Bits 0-14 == Ticks per quarter note
        ticks_per_quarter_note = (data_division & 0xEFFF)
        print("Ticks / Quarter Note: " + str(ticks_per_quarter_note))
    '''
    '''
    if HexArrayToDecimal(fileContent[15]) == 1:
        frames_per_second = HexArrayToDecimal(fileContent[8:15])
        ticks_per_frames = HexArrayToDecimal(fileContent[0:8])
        print("Frames / Second: " + str(frames_per_second))
        print("Ticks / Second " + str(ticks_per_frames))
    else:
        data_division = HexArrayToDecimal(fileContent[12:14])
        print("Division: " + str(data_division))
    '''