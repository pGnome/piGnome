import serial
xbee = serial.Serial('/dev/ttyAMA0',9600)
xbee.write('8\n')
