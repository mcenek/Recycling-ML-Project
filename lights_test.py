#method that tests the lights
#intended for use with the power relay board
#written by John Haas

import RPi.GPIO as GPIO
import datetime, time, board, os, signal, subprocess, threading, concurrent.futures, busio

#basic variables that set up the ultrasonic sensor
global dur
dur = 10
echo = 5
trig = 6

#pins associated to the different relays
#NOTE relay pins may keep other systems from working like a mic
Relay_CH1=21
Relay_CH2=20
Relay_CH3=26

#sets the raspberry pi settings correctly
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(echo, GPIO.IN) #pin that reads the proximity
GPIO.setup(trig, GPIO.OUT) #pin that triggers the proximity sensor
GPIO.setup(Relay_CH1, GPIO.OUT)
GPIO.setup(Relay_CH2, GPIO.OUT)
GPIO.setup(Relay_CH3, GPIO.OUT)

#allows the program to end upon KeyboardInterrupt
running = True

def main():
    global running
    while running:
        try:
            #measures distance from ultrasonic
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

            if distance < 15:
                #turns on lights for 5 seconds
                GPIO.output(Relay_CH1, GPIO.LOW)
                GPIO.output(Relay_CH2, GPIO.LOW)
                GPIO.output(Relay_CH3, GPIO.LOW)
                first=time.perf_counter()
                while(time.perf_counter() - first < 5):
                    print('test')
                GPIO.output(Relay_CH1, GPIO.HIGH)
                GPIO.output(Relay_CH2, GPIO.HIGH)
                GPIO.output(Relay_CH3, GPIO.HIGH)


        except KeyboardInterrupt:
            #turns off lights upon ctrl + c
            GPIO.output(Relay_CH1, GPIO.HIGH)
            GPIO.output(Relay_CH2, GPIO.HIGH)
            GPIO.output(Relay_CH3, GPIO.HIGH)

            running = False

if __name__ == '__main__':
    main()