from picamera import PiCamera
import time, board, busio, logging
import adafruit_adxl34x
import RPi.GPIO as GPIO
import os, signal, subprocess, threading, concurrent.futures, csv

camera = PiCamera()
Relay_Ch1 = 20
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)
acc = adafruit_adxl34x.ADXL345(i2c)
GPIO.setup(Relay_Ch1, GPIO.OUT)

start = False

#def stop_cam():
#	camera.stop_recording()

def run_cam():
#	os.system('raspivid -o vids/' + str(time) + '.h264 -t 10000')
	tim = time.time()
	tim = int(tim)
	tim = str(tim)
	#callback = None
#	timer = threading.Timer(10.0, stop_cam)
	try:
		camera.start_recording('/home/pi/Project/vids/' + tim + '.h264')
		time.sleep(10)
		camera.stop_recording()
	except:
		pass

def print_accel(file1):
	GPIO.setup(24, GPIO.OUT)
	GPIO.output(24, 0)
	time.sleep(0.00002)
	GPIO.output(24, 1)
	time.sleep(0.000005)
	GPIO.output(24, 0)
	GPIO.setup(24, GPIO.IN)

	while GPIO.input(24) == 0:
		time1 = time.time()

	while GPIO.input(24) == 1:
		end_time = time.time()

	duration = end_time - time1
	distance = duration * 17000
	time.sleep(0.05)
	print(distance)
	while distance < 10:
		print("%f %f %f" %acc.acceleration, file = file1)
		time.sleep(0.1)
		GPIO.setup(24, GPIO.OUT)
		GPIO.output(24, 0)
		time.sleep(0.00002)
		GPIO.output(24, 1)
		time.sleep(0.000005)
		GPIO.output(24, 0)
		GPIO.setup(24, GPIO.IN)

		while GPIO.input(24) == 0:
			time1 = time.time()

		while GPIO.input(24) == 1:
			end_time = time.time()

		duration = end_time - time1
		distance = duration * 17000
		time.sleep(.05)

def lights():
	GPIO.output(Relay_Ch1, GPIO.LOW)
	GPIO.setup(24, GPIO.OUT)
	GPIO.output(24, 0)
	time.sleep(0.00002)
	GPIO.output(24, 1)
	time.sleep(0.000005)
	GPIO.output(24, 0)
	GPIO.setup(24, GPIO.IN)
	time1 = 0
	end_time = 0
	while GPIO.input(24) == 0:
		time1 = time.time()

	while GPIO.input(24) == 1:
		end_time = time.time()

	duration = end_time - time1
	distance = duration * 17000
	time.sleep(0.05)
#	x = 5000
#	while x > 0:
#		x = x-1
	while distance > 10:
		GPIO.output(Relay_Ch1, GPIO.HIGH)
		GPIO.setup(24, GPIO.OUT)
		GPIO.output(24, 0)
		time.sleep(0.00002)
		GPIO.output(24, 1)
		time.sleep(0.000005)
		GPIO.output(24, 0)
		GPIO.setup(24, GPIO.IN)

		while GPIO.input(24) == 0:
			time1 = time.time()

		while GPIO.input(24) == 1:
			end_time = time.time()

		duration = end_time - time1
		distance = duration * 17000
		time.sleep(0.05)
	print("terminating lights thread")


def main():
	while True:
		GPIO.setup(24, GPIO.OUT)
		GPIO.output(24, 0)
		time.sleep(0.00002)
		GPIO.output(24, 1)
		time.sleep(0.000005)
		GPIO.output(24, 0)
		GPIO.setup(24, GPIO.IN)

		while GPIO.input(24) == 0:
			time1 = time.time()

		while GPIO.input(24) == 1:
			end_time = time.time()

		duration = end_time - time1
		distance = duration * 17000
		print(distance)

		if distance < 10 : #and start == False:
		#start = True
		#GPIO.output(Relay_Ch1, GPIO.LOW)
		#print(time)
#		with concurrent.futures.ThreadPoolExecutor() as executor:
#			future = executor.submit(run_cam)
#			start = future.result()
#			print(start)
		#cam = threading.Thread(target=run_cam)
		#cam.start()
		#print(cam.join())
		#subprocess.Popen('raspivid -o vids/' + str(time) + '.h264 -t 10000', stdout=subprocess.PIPE, shell=True)
		#start = cam.result()
#	print(start)

			time1 = time.time()
			time1 = int(time1)
			time1 = str(time1)
#		while distance < 10:
			with concurrent.futures.ThreadPoolExecutor(5) as executor:
				accel_data = open("accel/" + time1 + ".txt", "w")
#			future = executor.submit(print_accel(accel_data))
				future2 = executor.submit(lights())
#		print_accel(time1)
##		accel_data = open("accel/" + time1 + ".txt", "w")
		#print("%f %f %f" %acc.acceleration, file = accel_data)
#	time.sleep(0.1)

#	GPIO.output(Relay_Ch1, GPIO.HIGH)


#time.sleep(10)
#camera.stop_recording()
if __name__ == "__main__":
	main()
