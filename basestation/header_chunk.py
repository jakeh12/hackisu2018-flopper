from header_data import HeaderData

class HeaderChunk(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.type = (raw_data & 0xFFFFFFFF00000000000000000000) >> (10 * 8)
        self.length = (raw_data & 0x00000000FFFFFFFF000000000000) >> (6 * 8)
        self.data = HeaderData(raw_data & 0x0000000000000000FFFFFFFFFFFF)

        '''
        1 byte == 8 bits
        4 bytes == 8 * 4
        1 HEX character = 4 bits
        # Hex = (8*4)/4
        1 byte = 8 / 4 dig == 2
        '''
