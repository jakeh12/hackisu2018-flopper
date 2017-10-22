import serial
import time

ser = serial.Serial('/dev/tty.usbmodem0E21FE51', 115200)


for channel in range(0, 10):
  for pitch in range(23, 45):  
    ser.write([pitch, ((1 << 7) | channel)])
    print(pitch)
    time.sleep(0.1)
    ser.write([pitch, ((0 << 7) | channel)])
    #time.sleep(0.001)
  print('-----------------')
  print('channel: ' + str(channel)) 
ser.close()
