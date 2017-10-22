import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)

for i in range(33, 48):
    ser.write([i, ((1 << 7) | (i - 33))])     # Note 40
    time.sleep(1)

ser.close()
