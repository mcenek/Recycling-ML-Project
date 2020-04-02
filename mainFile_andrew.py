from picamera import PiCamera
from gps import *
from getkey import getkey, keys
import datetime, time, board, os, signal, subprocess, threading, concurrent.futures, busio
import adafruit_adxl34x
import RPi.GPIO as GPIO
import time

camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)
# acc = adafruit_adxl34x.ADXL345(i2c) #This is the line causing issues with vibration sensor

echo = 5
trig = 6
Relay_Ch1 = 20

global dur
dur = 10

GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(Relay_Ch1, GPIO.OUT)

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

def cam():
    GPIO.output(Relay_Ch1, GPIO.LOW)
    tim = datetime.datetime.now()
    tim = str(tim)
#    try:
#        if gpsp.get_current_value()['class'] == 'TPV':
#            lon = gpsp.get_current_value().lon
#            lat = gpsp.get_current_value().lat
#            gps_time = gpsp.get_current_value().time
#            print(lon, lat, gps_time)
#            file_name = str(lon) + ',' + str(lat) + ',' + str(gps_time)
#            print(file_name)
#    except:
#        pass
    GPIO.output(Relay_Ch1, GPIO.HIGH)
    try:
        camera.start_recording('/home/pi/Recycling-ML-Project/vids/test_andrew/' + tim + '.h264')
        #camera.start_recording('/home/pi/Recycling-ML-Project/vids/test/' + file_name + '.h264')
        time.sleep(dur)
        camera.stop_recording()
       # GPIO.output(Relay_Ch1, GPIO.LOW)
    except:
        print("Camera error")
        pass
    GPIO.output(Relay_Ch1, GPIO.LOW)

def print_accel():
    tim = datetime.datetime.now()
    tim = str(tim)
    prim_tim = datetime.datetime.now().second
    fin_tim = datetime.datetime.now().second
    
    #Constantly be taking in reading from accelerometer while in the time window
    #If not possible i.e. accel error, update finish time and pass error
    while fin_tim - prim_tim < dur:
        try:
            print("%f %f %f" %acc.acceleration, file = open("./accel/test/" + tim +".txt", "a"))
            #print("%f %f %f" %acc.acceleration, file = open("./accel/test/" + filename +".txt", "a"))
            fin_tim = datetime.datetime.now().second
        except:
            fin_tim = datetime.datetime.now().second
            #print("Unable to fetch vibration sensor reading, continuing")
            pass
    print("Completed duration of loop")
    
def mic():
    tim = datetime.datetime.now()
    tim = str(tim)
    name = tim + '.wav'
#    print(name)
    cmd = ["arecord", "-D", "plughw:1", "-c1", "-r", "48000", "-f", "S32_LE", "-t", "wav", "--duration=10", "-V", "mono", "-v", name]
    #cmd = f"arecord -D plughw:1 -c1 -r 48000 -f S32_LE -t wav --duration={dur} -V mono -v {name}"
    #subprocess.Popen(cmd, shell=True)
    subprocess.Popen(cmd)

"""
Main method

While loop that will continuously run, waiting for motion sensor to trigger collection
of the data.
"""
def main():
    previousCoordinates = "File_name_n_a"
    while True:
#        gpsp = GPSpoller()
#        gpsp.start()
#        key = getkey()
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(trig, GPIO.LOW)
        
        count = time.time()
        while GPIO.input(echo) == 0 and time.time() - count < 0.1:
            pulse = time.time()

        count = time.time()
        while GPIO.input(echo) == 1 and time.time() - count < 0.1:
            pulse_end = time.time()

        distance = round((pulse_end - pulse) * 17150, 2)
        tim = datetime.datetime.now()
        tim = str(tim)
        try:
            if gpsp.get_current_value()['class'] == 'TPV':
                lon = gpsp.get_current_value().lon
                lat = gpsp.get_current_value().lat
                gps_time = gpsp.get_current_value().time
#                print(lon, lat, gps_time)
                previousCoordinates = str(lon) + ',' + str(lat) + ',' + str(gps_time)
                #print(file_name)
        except:
            pass
        if distance < 15:
            print("distance less than 15, processing camera\n")
            thread1 = threading.Thread(target=cam, args=())
            thread1.start()

            thread2 = threading.Thread(target = print_accel, args=())
            thread2.start()

            thread3 = threading.Thread(target = mic, args=())
            thread3.start()
            
            thread1.join()
            thread2.join()
            thread3.join()
        
#        if key == 'c':
#            GPIO.output(Relay_Ch1, GPIO.LOW)
#            GPIO.output(Relay_Ch1, GPIO.HIGH)
#            sys.exit()

if __name__ == "__main__":
    gpsp = GPSpoller()
    gpsp.start()
    main()
