import serial
serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)
while True:
	response = serialport.read(size=1)
	print response

