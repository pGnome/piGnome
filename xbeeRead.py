import serial
serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)
while True:
	response = serialport.read(size=1)
	if response.__len__() > 0:
		print response
	else:
		print "length is 0"

