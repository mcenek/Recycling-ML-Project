from picamera import PiCamera
import RPi.GPIO as GPIO
import time, datetime

camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

global dur
dur = 10
Relay_Ch1 = 20

GPIO.setup(Relay_Ch1, GPIO.OUT)

GPIO.output(Relay_Ch1, GPIO.HIGH)
try:
    tim = datetime.datetime.now()
    print("started recording")
    camera.framerate=12
    camera.shutter_speed=3000
    camera.iso=700
    spd=camera.shutter_speed
    print(str(spd))
    print(str(camera.framerate))
    print(str(camera.iso))
    camera.start_recording('/home/pi/Recycling-ML-Project/vids/test_john/' + str(tim) + '.h264')
    #time.sleep(dur)
    camera.wait_recording(dur)
    camera.stop_recording()
    print("stopped recording")
except:
    print("general camera error, continuing")
    camera.stop_recording()
    pass

GPIO.setmode(GPIO.BCM)
GPIO.output(Relay_Ch1, GPIO.LOW)