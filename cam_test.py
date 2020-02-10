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

global dur
dur= 10

GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(Relay_Ch1, GPIO.OUT)

def cam():
    GPIO.output(Relay_Ch1, GPIO.LOW)
    tim = datetime.datetime.now()
    tim = str(tim)
    GPIO.output(Relay_Ch1, GPIO.HIGH)
    try:
        camera.start_recording('/home/pi/Recycling-ML-Project/vids/test/' + tim + '.h264')
        time.sleep(dur)
        camera.stop_recording()
        GPIO.output(Relay_Ch1, GPIO.LOW)
    except:
        pass

def print_accel():
    tim = datetime.datetime.now()
    tim = str(tim)
    prim_tim = datetime.datetime.now().second
    fin_tim = datetime.datetime.now().second
    while fin_tim - prim_tim < dur:
        print("%f %f %f" %acc.acceleration, file = open("/home/pi/Recycling-ML-Project/accel/test/" + tim +".txt", "a"))
        fin_tim = datetime.datetime.now().second

def mic():
    tim = datetime.datetime.now()
    tim = str(tim)
    name = tim + '.wav'
    print(name)
    cmd = f"arecord -D plughw:1 -c1 -r 48000 -f S32_LE -t wav --duration={dur} -V mono -v {name}"
    subprocess.Popen(cmd, shell=True)

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
            thread1 = threading.Thread(target=cam, args=())
            thread1.start()

            thread2 = threading.Thread(target = print_accel, args=())
            thread2.start()

            thread3 = threading.Thread(target = mic, args=())
            thread3.start()
            
            thread1.join()
            thread2.join()
            thread3.join()


if __name__ == "__main__":
    main()
