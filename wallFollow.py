import socket
import time
from gpiozero import CamJamKitRobot, DistanceSensor
import math
import warnings

# warnings.filterwarnings("ignore")

robot = CamJamKitRobot()
initialDistance = math.inf
mode = "stop"


def forward(robot, speed=1):
	robot.value = (1 * speed, 0.9 * speed)


def stop(robot):
	robot.stop()


def left(robot, speed=1.0):
	robot.value = (1 * speed, -1 * speed)


def right(robot, speed=1.0):
	robot.value = (-1 * speed, 1 * speed)


def slightLeft(robot, speed, powDiff=0.0):
	speedModifier = 1 + powerDiff
	min(speedModifier, 2)
	robot.value = (speed * 0.95, speed * 0.9 * speedModifier)


def slightRight(robot, speed, powDiff=0.0):
	speedModifier = 1 + powerDiff
	min(speedModifier, 2)
	robot.value = (speed * 1 * speedModifier, speed * 0.85)


def getDistance():
	with warnings.catch_warnings():
		try:
			pinTrigger = 17
			pinEcho = 18
			sensor = DistanceSensor(echo=pinEcho, trigger=pinTrigger)
			return sensor.distance
		except:
			return -1
	return -1


def scan():
	print("Getting initial wall distance")
	count = 0
	global initialDistance

	for i in range(25):
		EPSILON = 1.1
		left(robot, 0.4)
		time.sleep(0.2)
		stop(robot)
		currentDistance = getDistance()
		print(currentDistance)
		if currentDistance < initialDistance and currentDistance != -1:
			initialDistance = currentDistance
			count = i
		time.sleep(0.1)

	stop(robot)

	print("Shortest distance is %f" % initialDistance)

	for i in range(24 - count):
		right(robot, 0.4)
		time.sleep(0.2)
		stop(robot)
		time.sleep(0.2)


def modeSetter():
	TCP_IP = '192.168.99.13'
	TCP_PORT = 8080
	BUFFER_SIZE = 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(2)

	print("waiting for commands")
	while True:
		conn, addr = s.accept()
		data = conn.recv(BUFFER_SIZE).decode("ascii").strip()
		if data != "getdist" and data != "getmotors":
			print(data)
			global mode
			mode = data
		else:
			response = data
			if data == "getdist":
				response = str(getDistance()).encode()
			elif data == "getmotors":
				response = str(robot.value).encode()
			else:
				print(data)

			print(response)
			conn.send(response)

		conn.close()

from _thread import start_new_thread

start_new_thread(modeSetter, ())

while True:

	if mode == "start":
		if initialDistance == math.inf:
			initialDistance = getDistance()

		if initialDistance == -1.0 or initialDistance == 1.0:
			scan()
			continue

		distance = getDistance()

		powerDiff = abs(distance - initialDistance)

		if distance == -1:
			time.sleep(0.1)
		elif distance < initialDistance:
			slightRight(robot, 0.4, powerDiff)
		else:
			slightLeft(robot, 0.6, powerDiff)
	elif mode == "stop":
		stop(robot)
	elif mode == "scan":
		scan()
		mode = "stop"
	elif mode == "reset":
		initialDistance = getDistance()
		mode = "stop"
