import serial
serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)
while True:
	response = serialport.read(size=26)
	if response.__len__() > 0:
		for c in response:
			print ord(c)
	else:
		print "length is 0"

