import RPi.GPIO as GPIO
import time
import datetime

def testLights():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.LOW) #Turn off to start
    time.sleep(2)
    GPIO.output(20, GPIO.HIGH) #Turn on for 5 seconds, then turn off
    print("curr running")
    time.sleep(5)
    GPIO.output(20, GPIO.LOW)

def testTiming():
    start = time.time()
    time.sleep(5)
    end = time.time()
    elapsed = end - start
    print(f"start: {start}\tend: {end}\telapsed: {elapsed}")

try:
    testLights()
except KeyboardInterrupt:
    print("keyboard interrupted")
    GPIO.output(20, True)
    print("GPIO turned off, exiting")
    exit()

#testTiming()
#print(type(datetime.datetime.now()))
#print(type(time.time()))