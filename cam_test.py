from picamera import PiCamera
import datetime, time, board, os, signal, subprocess, threading, concurrent.futures, busio
import adafruit_adxl34x
import RPi.GPIO as GPIO

camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)
acc = adafruit_adxl34x.ADXL345(i2c)

echo = 5
trig = 6
Relay_Ch1 = 20

GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(Relay_Ch1, GPIO.OUT)

def cam():
    GPIO.output(Relay_Ch1, GPIO.LOW)
    tim = datetime.datetime.now()
    #tim = int(tim)
    tim = str(tim)
    GPIO.output(Relay_Ch1, GPIO.HIGH)
    try:
        camera.start_recording('/home/pi/Project/vids/test/' + tim + '.h264')
    #timer = threading.Timer(100, main)
    #timer.start()
        time.sleep(10)
        camera.stop_recording()
        GPIO.output(Relay_Ch1, GPIO.LOW)
    except:
        pass

def print_accel():
    tim = datetime.datetime.now()
    tim = str(tim)
    #print(tim)
    #file1 = ("/home/pi/Project/accel/test/" + tim + ".csv")
    #print(file1
    #try:
    while thread1.is_alive():
        print("%f %f %f" %acc.acceleration, file = open("/home/pi/Project/accel/test/" + tim +".txt", "a"))
    #except:
    #pass

#thread1 = threading.Thread(target=cam, args=())
#thread2 = threading.Thread(target = print_accel, args=())

def main():
    while True:
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
        #print(distance)
        tim = datetime.datetime.now()
        tim = str(tim)

        if distance < 15:
            global thread1 
            thread1 = threading.Thread(target=cam, args=())
            #thread1
            thread1.start()
            #with open("/home/pi/Project/accel/test/" + tim + ".txt", "w") as f:
            #while thread1.is_alive():#this needs to be threaded because the printing blocks the code
                #print("%f %f %f" %acc.acceleration, file = open("/home/pi/Project/accel/test/" + tim +".txt", "a"))
                #print("hi")

            thread2 = threading.Thread(target = print_accel, args=())
            thread2.start()
            #while thread1.isAlive():
            #thread2
                #thread2.start()
            
            #thread1.join()
            #thread2.join()


if __name__ == "__main__":
    main()
