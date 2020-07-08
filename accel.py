#function that tests the accelerometer
#written by Dan Moldaovan

import time
import board
import busio
import adafruit_adxl34x
#turns on the accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    #prints the acceleration
	print("%f %f %f"%accelerometer.acceleration)
	time.sleep(0.1)