byte_size = 8

def HexArrayToDecimal(hex_list):
    dec_value = 0
    shift_amount = ((len(hex_list) - 1) * byte_size)

    for hex_byte in hex_list:
        temp_value = ord(hex_byte) << shift_amount
        dec_value = dec_value | temp_value
        shift_amount -= byte_size

    return dec_value

with open('/home/justin/Documents/happy_birthday.mid', 'rb') as midiFile:
    fileContent = list(midiFile.read())

    # Parse header chunk
    # Type (4 bytes) - Length (4 bytes) - Data (2 / 2 / 2 bytes)
    header_type = HexArrayToDecimal(fileContent[0:4])
    header_length = HexArrayToDecimal(fileContent[4:8])
    data_format = HexArrayToDecimal(fileContent[8:10])
    data_tracks = HexArrayToDecimal(fileContent[10:12])
    data_division = HexArrayToDecimal(fileContent[12:14])

    print("Header Length: " + str(header_length))
    print("Format: " + str(data_format))
    print("# Tracks: " + str(data_tracks))
    print("Division: " + str(data_division))