#tests the ultrasonice sensor by itself
#written by John Haas

import RPi.GPIO as GPIO
import datetime, time, board, os, signal, subprocess, threading, concurrent.futures, busio

#pins for ultrasonic sensor
echo = 5
trig = 6

#necessary for setting pi settings correctly
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(echo, GPIO.IN) #pin that reads the proximity
GPIO.setup(trig, GPIO.OUT) #pin that triggers the proximity sensor

running = True

def main():
    #allows the thread to be ended upon KeyboardInterrupt
    global running
    while running:
        try:
            #reads the distance from the ultrasonic sensor
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

            #tells you whether the ultrasonic sensor is being triggered or not
            if distance < 15:
                print('test')
            else:
                print('still test')

        except KeyboardInterrupt:
            running = False

if __name__ == '__main__':
    main()