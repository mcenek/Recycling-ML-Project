import numpy as np
import threading as thread
import time

class threadingDevice:
    #Where all the global variables will be stored
    def __init__(self, GPS_update_interval, proximity_threshold, proximity_timer, record_time, terminate_threshold):
        #Global variables to be defined by user (can create constants after testing has been done)
        self.GPS_update_interval = GPS_update_interval
        self.proximity_threshold = proximity_threshold
        self.proximity_timer = proximity_timer
        self.record_time = record_time
        self.terminate_threshold = terminate_threshold

        #Constants to be shared between classes
        self.bool_start_recording = False
        self.bool_run = True
        self.GPS_coord_lat = None
        self.GPS_coord_long = None
        self.current_time = None

    #Method that will control the camera thread
    def camera():
        print('camera')
        while self.record_time < 15:
            
    
    #Method that will control the accelerometer
    def accelerometer():
        print('accelerometer')
    
    #Method that controls the lights
    def lights():
        print('lights')

    #Method that controls the sound
    def sound():
        print('sound')

    #gps tracking thread
    def gps():
        print('gps')

    #Method that indicates when motion sensor is activated
    def armTrigger():
        print('armTrigger')
        # while(self.bool_run):

    arm_trigger_thread = thread.Thread(target=armTrigger, args=())
    gps_thread = thread.Thread(target=gps, args=())
    camera_thread = thread.Thread(target=camera, args=())
    sound_thread = thread.Thread(target=sound, args=())

    #Main method where everything is brought together
    def main(self):
        self.arm_trigger_thread.start()
        self.gps_thread.start()
        self.camera_thread.start()
        self.sound_thread.start()
        while(self.bool_run):
            
            
        print('main method')
    
if __name__ == '__main__':
    device = threadingDevice(GPS_update_interval=10, proximity_threshold=10, proximity_timer=5, record_time=3, terminate_threshold=15)
    device.main()
