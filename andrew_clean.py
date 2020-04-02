from picamera import PiCamera
from gps import *
from getkey import getkey, keys
import datetime, time, board, os, signal, subprocess, threading, concurrent.futures, busio
import adafruit_adxl34x
import RPi.GPIO as GPIO
import time

"""
Initialize all our important settings
Camera, GPIO mode, accelorometer
"""
camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)
acc = adafruit_adxl34x.ADXL345(i2c)

"""
Global definition for time window of recording/reading information
"""
global dur
dur = 10


"""
Set up of GPIO pins
"""
GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(Relay_Ch1, GPIO.OUT)

"""
Class GPSpoller
Will continuously be pulling/reading in the GPS coordinates
Separate class since this will always be running due to extended boot time if turned on/off
"""
class GPSpoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None

    def get_current_value(self):
        return self.current_value

    def run(self):
        try:
            while True:
                self.current_value = self.session.next()
                time.sleep(0.2)

        except StopIteration:
            pass

"""
Class manageUtilities
Manages all the pieces of the project besides the GPS
"""
class manageUtilities:
    def __init__(self, gpsTracker):
        self.gpsTracker = gpsTracker
        
    