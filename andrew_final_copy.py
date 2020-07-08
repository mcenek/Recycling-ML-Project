from picamera import PiCamera
from gps import *
import datetime, time, board, os, signal, subprocess, threading, concurrent.futures, busio
import adafruit_adxl34x
import RPi.GPIO as GPIO



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
dur = 10 #in seconds
stale_limit=5 #in seconds
stale_reset_distance=0.00001
echo = 5
trig = 6

#Relay_Ch1 = 21 #Uncomment if using relay board

running = True #used for keyboard interrupt
time_sync = False #used for determining whether to use perfs or time

"""
Set up of GPIO pins
"""
GPIO.setup(echo, GPIO.IN) #pin that reads the proximity
GPIO.setup(trig, GPIO.OUT) #pin that triggers the proximity sensor
#GPIO.setup(Relay_Ch1, GPIO.OUT) #uncomment for relay channels

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
        self.set_of_values = [None, None] #current_value, perf_counter

    def get_current_value(self):
        return self.current_value

    def get_set_of_values(self):
        return self.set_of_values

    """
    function that sends that records the current gps data and determines if its stale
    """
    def upload_data(self, glob_time):
        print('Trying to upload')
        global stale_limit

        new_perf = time.perf_counter()

        #makes sure the gps has at least gotten one reading
        if self.set_of_values[0] == None:
            file_text = "Current perf: " + str(new_perf)
            print(file_text, file = open('/home/pi/Recycling-ML-Project-johns_testing/stop_locations/' + str(glob_time) + '.txt', 'a'))
            return

        #gets values necessary for the print statement
        perf_recorded = self.set_of_values[1]
        latitude = getattr(self.set_of_values[0], 'lat', 0.0)
        longitude = getattr(self.set_of_values[0], 'lon', 0.0)
        time_recorded = getattr(self.set_of_values[0], 'time', '')

        #prints data to file while determining if it is stale
        if time.perf_counter() - perf_recorded < stale_limit:
            print('not stale')
            file_text = "First Perf: " + str(perf_recorded) + "\nLatitude: " + str(latitude) + "\nLongitude: " + str(longitude) + "\nFirst Time: " +  time_recorded + "\nCurrent perf: " + str(new_perf)
            print(file_text, file = open('/home/pi/Recycling-ML-Project-johns_testing/stop_locations/' + str(glob_time) + '.txt', 'a'))
        else:
            print('stale')
            file_text = "First Perf: " + str(perf_recorded) + "\nLatitude: " + str(latitude) + "\nLongitude: " + str(longitude) + "\nFirst Time: " +  time_recorded + "\nCurrent perf: " + str(new_perf) + "\nData is stale"
            print(file_text, file = open('/home/pi/Recycling-ML-Project-johns_testing/stop_locations/' + str(glob_time) + '.txt', 'a'))

    """
    what will constantly happen as the program runs
    """
    def run(self):
        #default values
        global time_sync
        global stale_reset_distance
        old_lat=-1000
        old_lon=-1000

        try:
            while running:
                self.current_value = self.session.next()
                #only happens if the gps gets a reading
                if (self.current_value != None):
                    if getattr(self.current_value, 'lat', 0.0) != 0.0:
                        latitude = getattr(self.current_value, 'lat', 0.0)
                        longitude = getattr(self.current_value, 'lon',0.0)
                        #only happens if this is not the first reading
                        if(self.set_of_values[0] != None):
                            old_lat = getattr(self.set_of_values[0], 'lat', 0.0)
                            old_lon = getattr(self.set_of_values[0], 'lon', 0.0)
                        #only happens if this is first reading
                        if(self.current_value['class'] == 'TPV' and time_sync == False):
                            strt_time = "Perf Counter:" + str(time.perf_counter()) +'\nStartup Time:' + getattr(self.current_value, 'time', '')
                            print(strt_time + "\nLatitude: " + str(latitude) + "\nLongitude: " + str(longitude), file = open('/home/pi/Recycling-ML-Project-johns_testing/gps_startup_times/' + str(time.time()) + '.txt', 'a'))
                            self.set_of_values = [self.current_value, time.perf_counter()]
                            time_sync = True
                        #only updates set_of_values if gps has been moving
                        elif(self.current_value['class'] == 'TPV' and (abs(float(latitude) - float(old_lat)) >= stale_reset_distance or abs(float(longitude) - float(old_lon)) >= stale_reset_distance)):
                            print("changing data")
                            self.set_of_values[0]=self.current_value
                            self.set_of_values[1]=time.perf_counter()
                            old_lat = getattr(self.current_value, 'lat', 0.0)
                            old_lon = getattr(self.current_value, 'lon', 0.0)
                        else:
                            pass
                    time.sleep(0.2)

        except StopIteration:
            pass

"""
Remaining code manages all the pieces of the project besides the GPS
"""

#handles camera recording
def cam(tim):
    #GPIO.output(Relay_Ch1, GPIO.LOW) #change back to low
    tim = str(tim)
    #GPIO.output(Relay_Ch1, GPIO.HIGH)

    #if camera is working record video for the expected amount of time
    try:
        camera.start_recording('/home/pi/Recycling-ML-Project-johns_testing/vids/test_john/' + tim + '.h264')
        camera.wait_recording(dur)
        camera.stop_recording()
    except:
        print("general camera error, continuing")
        camera.stop_recording()
        pass

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(Relay_Ch1, GPIO.OUT)
    #GPIO.output(Relay_Ch1, GPIO.LOW)

"""
function that records the accelerometer data
"""
def print_accel(tim):
    global acc
    global properACCBoot
    global running

    prim_tim = time.perf_counter()
    fin_tim = time.perf_counter()
    tim = str(tim)

    #Constantly be taking in reading from accelerometer while in the time window
    #If not possible i.e. accel error, update finish time and pass error
    print(fin_tim - prim_tim)
    print(dur)
    while fin_tim - prim_tim < dur and running:
        try:
            print("%f %f %f" %acc.acceleration, file = open("/home/pi/Recycling-ML-Project-johns_testing/accel/johns_tests/" + tim +".txt", "a"))
            print("%f" %(fin_tim-prim_tim), file = open("/home/pi/Recycling-ML-Project-johns_testing/accel/johns_tests/" + tim +".txt", "a"))
            #print("%f %f %f" %acc.acceleration, file = open("./accel/test/" + filename +".txt", "a"))
            fin_tim = time.perf_counter()
            time.sleep(0.01)
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

"""
function that records the microphone information
"""
def mic(tim):
    global running
    print("entered mic method")
    #runs a subprocess that records mic information
    name = '/home/pi/Recycling-ML-Project-johns_testing/microphone/' + str(tim) + '.wav'
    cmd = ['/home/pi/Recycling-ML-Project-johns_testing/mic.sh', name]
    p1=subprocess.Popen(cmd)
    while running == True and p1.poll() == None:
        continue
    #handles keyboard interrupt
    #NOTE eventually work to interrupt subprocess
    if p1.poll() == None:
        print("terminated")
        p1.send_signal(signal.SIGINT)
    print("Finished recording sound")

#Just to get the official start time that will be fed into all the threads
def globalTimer():
    global gpsp
    global time_sync
    report=gpsp.get_current_value()
    if report['class'] == 'TPV':
        return getattr(report, 'time', '')
    elif time_sync:
        return str(datetime.datetime.now())
    else:
        return time.perf_counter()

"""
Main method

While loop that will continuously run, waiting for motion sensor to trigger collection
of the data.
"""
def main():
    global running
    global gpsp

    previousCoordinates = "File_name_n_a"

    #keeps us from getting wierd errors
    report=None
    while(report == None):
        report=gpsp.get_current_value()

    first_perf= time.perf_counter()
    if report['class'] == 'TPV':
        start= getattr(report, 'time', '')
        latitude = report.lat
        longitude = report.lon
        file_text = 'Time: '+ start + '\nPerf: ' + first_perf + '\nLatitude: ' + latitude + '\nLongitude: ' + longitude
        print(file_text, file = open("/home/pi/Recycling-ML-Project-johns_testing/starting_states/" + str(start) + " " + str(first_perf) + ".txt", "a"))
    else:
        print('Perf: ' + str(first_perf), file = open("/home/pi/Recycling-ML-Project-johns_testing/starting_states/" + str(first_perf) + ".txt", "a"))

    while running:
        try:
            GPIO.output(trig, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(trig, GPIO.LOW)

            count = time.perf_counter()
            pulse = time.perf_counter()
            while GPIO.input(echo) == 0 and pulse - count < 0.1:
                pulse = time.perf_counter()

            count = time.perf_counter()
            pulse_end = time.perf_counter()
            while GPIO.input(echo) == 1 and pulse_end - count < 0.1:
                pulse_end = time.perf_counter()

            distance = round((pulse_end - pulse) * 17150, 2) #converts to cm

            globalTime = globalTimer()

            if distance < 15:

                gpsp.upload_data(globalTime)
                #GPIO.output(Relay_Ch1, GPIO.HIGH)
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

                #GPIO.output(Relay_Ch1, GPIO.LOW)
                print("Video successfully captured")

        except KeyboardInterrupt:
            running=False

            print("keyboard interrupt, program terminating")
            activeThreads = threading.enumerate()
            print(activeThreads)
            #GPIO.output(Relay_Ch1, GPIO.LOW) #Turn off Relay Board
            GPIO.cleanup()
            sys.exit()

if __name__ == "__main__":
    gpsp = GPSpoller()
    gpsp.start()
    main()