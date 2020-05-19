from picamera import PiCamera
from gps import *
# from getkey import getkey, keys
import datetime, time, board, os, signal, subprocess, threading, concurrent.futures, busio
import adafruit_adxl34x
import RPi.GPIO as GPIO
import time


"""
Initialize/setup all our important items
Camera, GPIO mode, accelorometer, mic
"""
camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)

#NOTE: Connection may be loose, make sure accelerometer pressed securely in
#Variable to track whether acc was properly booted or not
properACCBoot = 0
try:
    acc = adafruit_adxl34x.ADXL345(i2c)
    properACCBoot = 1
except:
    print("Will attempt acc reboot later")
    pass

"""
Global definition for time window of recording/reading information and other info
"""
global dur
dur = 10
echo = 5
trig = 6
Relay_Ch1 = 20 #Currently using relay channel 2 on relay board, variable name not updated

running = True

"""
Set up of GPIO pins
"""
GPIO.setup(echo, GPIO.IN) #pin that reads the proximity
GPIO.setup(trig, GPIO.OUT) #pin that triggers the proximity sensor
GPIO.setup(Relay_Ch1, GPIO.OUT) #the relay channels

"""
Class GPSpoller
Will continuously be pulling/reading in the GPS coordinates
Separate class since this will always be running due to extended boot time if turned on/off
"""
class GPSpoller(threading.Thread):

    def end_thread(self):
        running=False

    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None

    def get_current_value(self):
        return self.current_value

    def run(self):
        try:
            while running:
                self.current_value = self.session.next()
                time.sleep(0.2)

        except StopIteration:
            pass

"""
Remaining code manages all the pieces of the project besides the GPS
"""

#Need a way to turn everything off/stop listening for new motion while tracking a current stop

def cam(tim):
    #NOTE: adjust date/time pulling because no internet access on live routes
    #GPIO.output(Relay_Ch1, GPIO.LOW) #change back to low
#     tim = datetime.datetime.

    tim = str(tim)

    #GPIO.output(Relay_Ch1, GPIO.HIGH)
    try:
        camera.start_recording('/home/pi/Recycling-ML-Project/vids/test_john/' + tim + '.h264')
        #time.sleep(dur)
        camera.wait_recording(dur)
        camera.stop_recording()
    except:
        print("general camera error, continuing")
        camera.stop_recording()
        pass

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(Relay_Ch1, GPIO.OUT)
    #GPIO.output(Relay_Ch1, GPIO.LOW)

def print_accel(tim):
    global acc
    global properACCBoot

#     tim = datetime.datetime.now()
#     tim = str(tim)
    prim_tim = time.perf_counter()
    fin_tim = time.perf_counter()
    tim = str(tim)

    #Constantly be taking in reading from accelerometer while in the time window
    #If not possible i.e. accel error, update finish time and pass error
    print(fin_tim - prim_tim)
    print(dur)
    while fin_tim - prim_tim < dur:
        try:
            print("%f %f %f" %acc.acceleration, file = open("./accel/johns_tests/" + tim +".txt", "a"))
            #print("%f %f %f" %acc.acceleration, file = open("./accel/test/" + filename +".txt", "a"))
            fin_tim = time.perf_counter()
        except:
            fin_tim = time.perf_counter()
            #If global definition of properACCBoot is still 0, try and see if connected for next iteration

            if properACCBoot == 0:
                try:
                    acc = adafruit_adxl34x.ADXL345(i2c)
                    properACCBoot = 1
                except:
                    pass

    print("Finished gathering accelerometer data")

def mic(tim):
#     tim = datetime.datetime.now()
#     tim = str(tim)
    print("entered mic method")
    name = str(tim) + '.wav'
#    print(name)
    cmd = ["arecord", "-D", "plughw:1", "-c1", "-r", "48000", "-f", "S32_LE", "-t", "wav", "--duration=10", "-V", "mono", "-v", name]
    #cmd = f"arecord -D plughw:1 -c1 -r 48000 -f S32_LE -t wav --duration={dur} -V mono -v {name}"
    #subprocess.Popen(cmd, shell=True)
    print("mic method step 2")
    subprocess.Popen(cmd)
    print("mic method ended")

#Just to get the official start time that will be fed into all the threads
def globalTimer():
    return datetime.datetime.now()
#    return time.time()

"""
Main method

While loop that will continuously run, waiting for motion sensor to trigger collection
of the data.
"""
def main():
    global running

    previousCoordinates = "File_name_n_a"
    while running:
        try:
            GPIO.output(trig, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(trig, GPIO.LOW)

            count = time.time()
            while GPIO.input(echo) == 0 and time.time() - count < 0.1:
                pulse = time.time()

            count = time.time()
            while GPIO.input(echo) == 1 and time.time() - count < 0.1:
                pulse_end = time.time()

            distance = round((pulse_end - pulse) * 17150, 2) #converts to cm
            tim = datetime.datetime.now()
            tim = str(tim)
            try:
                if gpsp.get_current_value()['class'] == 'TPV':
                    lon = gpsp.get_current_value().lon
                    lat = gpsp.get_current_value().lat
                    gps_time = gpsp.get_current_value().time
    #               print(lon, lat, gps_time)
                    previousCoordinates = str(lon) + ',' + str(lat) + ',' + str(gps_time)
                    #print(file_name)
            except:
                pass
            globalTime = globalTimer()

            if distance < 15:

                GPIO.output(Relay_Ch1, GPIO.HIGH)
                print("distance less than 15, processing camera\n")
                thread1 = threading.Thread(name='cam_thread', target=cam, args=(globalTime,))
                thread1.start()

                thread2 = threading.Thread(name='accel_thread', target = print_accel, args=(globalTime,))
                thread2.start()

                thread3 = threading.Thread(name='mic_thread', target = mic, args=(globalTime,))
                thread3.start()

                thread1.join()
                thread2.join()
                thread3.join()

                GPIO.output(Relay_Ch1, GPIO.LOW)
                print("Video successfully captured")

        except KeyboardInterrupt:
            running=False

            print("keyboard interrupt, program terminating")
            activeThreads = threading.enumerate()
            print(activeThreads)
            GPIO.output(Relay_Ch1, GPIO.LOW) #Turn off Relay Board
            GPIO.cleanup()
            sys.exit()

if __name__ == "__main__":
    gpsp = GPSpoller()
    gpsp.start()
    main()