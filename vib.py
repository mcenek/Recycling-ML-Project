import RPi.GPIO as GPIO
import time

chan = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(chan, GPIO.IN)

def callback(chan):
	if GPIO.input(chan):
		print("Vibration")
	else:
		print("vib")

GPIO.add_event_detect(chan, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(chan, callback)

while True:
	time.sleep(1)
