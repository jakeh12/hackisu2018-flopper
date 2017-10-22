def HexArrayToDecimal(hex_list):
    dec_value = 0
    byte_size = 8
    shift_amount = ((len(hex_list) - 1) * byte_size)

    for hex_byte in hex_list:
        temp_value = ord(hex_byte) << shift_amount
        dec_value = dec_value | temp_value
        shift_amount -= byte_size

    return dec_value

def OctaveMatch(value):
    '''
    while value > 48:
        value -= 12

    while value < 33:
        value += 12
    '''
    return value
