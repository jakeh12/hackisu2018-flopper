from helpers import HexArrayToDecimal

class TrackData(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.temp = list()
        self.parse_events()

    def parse_events(self):
        byte_pointer = 0
        delta_time = 0
        time_parsing = True
        relative_time = 0

        while byte_pointer < len(self.raw_data):
            current_byte = HexArrayToDecimal(self.raw_data[byte_pointer])

            if time_parsing:
                if (current_byte & 0x80) == 0:
                    # Found end of delta time
                    relative_time += delta_time
                    #print("Delta Time: " + str(delta_time))
                    #print("Relative Time: " + str(relative_time))
                    delta_time = 0
                    time_parsing = False
                else:
                    delta_time = delta_time << 8
                    delta_time = delta_time | current_byte
            else:
                channel_mask = (current_byte & 0xF0)
                sysex_mask = (current_byte & 0xFF)

                if channel_mask == 0x90:
                    note = HexArrayToDecimal(self.raw_data[byte_pointer + 1])
                    print("Note on: " + str(note) + " @ " + str(relative_time))
                    byte_pointer += 2
                elif channel_mask == 0x80:
                    note = HexArrayToDecimal(self.raw_data[byte_pointer + 1])
                    print("Note off: " + str(note) + " @ " + str(relative_time))
                    byte_pointer += 2
                elif channel_mask == 0xA0:
                    print("Polyphonic Key Pressure")
                    byte_pointer += 2
                elif channel_mask == 0xB0:
                    print("Controller Change OR Mode")
                    byte_pointer += 2
                elif channel_mask == 0xC0:
                    print("Program Change")
                    byte_pointer += 1
                elif channel_mask == 0xD0:
                    print("Channel Key Pressure")
                    byte_pointer += 1
                elif channel_mask == 0xE0:
                    print("Pitch Bend")
                    byte_pointer += 2
                elif sysex_mask == 0xF0:
                    print("F0 -- ???")
                elif sysex_mask == 0xF7:
                    print("F7 -- ???")

                time_parsing = True
            byte_pointer += 1
