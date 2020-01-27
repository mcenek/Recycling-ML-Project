import serial, time, string, pynmea2

while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata = ser.readline()

	if newdata[0:6] == "$GPGLL":
		newmsg = pynmea2.parse(newdata)
		lat = newmsg.latitude
		lng = newmsg.longitude
		gps = "Lat =" + str(lat) + "and Long =" + str(lng)
		print(gps)
