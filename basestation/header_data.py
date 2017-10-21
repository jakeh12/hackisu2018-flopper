class HeaderData(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.format = (raw_data & 0xFFFF00000000) >> (4 * 8)
        self.tracks = (raw_data & 0x0000FFFF0000) >> (2 * 8)
        self.division_format = (raw_data & 0x000000008000)

        # Check to see if bit 15 is 1 or 0
        if self.division_format == 1:
            # Bit 15 == 1
            # Bits 8-14 == -frames/second
            # Bits 0-7 == ticks/frame
            self.frames_per_second = (raw_data & 0x00000000EF00) >> 8
            self.ticks_per_frame = (raw_data & 0x0000000000FF)
        else:
            # Bit 15 == 0
            # Bits 0-14 == Ticks per quarter note
            self.ticks_per_quarter_note = (raw_data & 0x00000000EFFF)
