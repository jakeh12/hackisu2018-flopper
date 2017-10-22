import serial
from helpers import OctaveMatch

class DriveSystem(object):
    def __init__(self):
        # Information stored in tuple: (available, startTime, note)
        self.available_drives = [(1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0),
                                 (1, 0, 0)]
        self.ser = serial.Serial('/dev/tty.usbmodem0E21FE51', 115200)

    def find_available_drive(self):
        for i in range(0, len(self.available_drives)):
            if self.available_drives[i][0] == 1:
                return i

        # Couldn't find an available drive
        return -1

    def lock_drive(self, drive_num, note):
        if drive_num == -1:
            print("Invalid drive")
            return

        self.available_drives[drive_num] = (0, note[1], note[0])
        note = OctaveMatch(note[0])
        self.ser.write([note, ((1 << 7) | drive_num)])
        print("SENDING: (note = " + str(note) + ", drive = " + str(drive_num) + ", on = 1")

    def find_playing_drive(self, note):
        for i in range(0, len(self.available_drives)):
            if self.available_drives[i][0] == 0 and self.available_drives[i][2] == note[0]:
                return i

        # Couldn't find the drive playing the specified note
        return -1

    def unlock_drive(self, drive_num, note):
        if drive_num == -1:
            print("Invalid drive")
            return

        self.available_drives[drive_num] = (1, 0, 0)
        note = OctaveMatch(note[0])
        self.ser.write([note, (0x7F & drive_num)])
        print("SENDING: (note = " + str(note) + ", drive = " + str(drive_num) + ", on = 0")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.close()


