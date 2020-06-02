import board, os, signal, subprocess, threading, concurrent.futures, busio
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

Relay=21

GPIO.setup(Relay, GPIO.OUT)

def mic():
    print("start")
    cmd = ['./camera.sh', 'file2.wav']
    p1=subprocess.run(cmd, shell=False)

def main():
    #thread1 = threading.Thread(name='cam_thread', target=mic)
    #thread1.start()
    #thread1.join()
    thread1 = threading.Thread(name='mic_thread', target = mic)
    thread1.start()
    thread1.join()

if __name__ == "__main__":
    main()