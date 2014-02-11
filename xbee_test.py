import serial

ser = serial.Serial('/dev/ttyAMA0', 9600)
string = 'Hello from Raspberry Pi'
print 'Sending "%s"' % string
ser.write('%s\n' % string)

while True:
	incoming = ser.readline().strip()
	print 'Received %s' % incoming
	ser.write('RPI Received: %s\n' % incoming)

