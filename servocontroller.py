from gpiozero import Servo
from threading import Thread, Lock
import time
import math
import sys

class ServoController(Thread):
	def __init__(self, pin=14, frequency=1, minimum=-0.2, maximum=1, resting=1):
		Thread.__init__(self)
		self.servo = Servo(pin)
		self.servo.value = None
		self.servo_reset_delay = 0.5
		
		self.frequency = frequency
		self.minimum = minimum
		self.maximum = maximum
		self.resting = resting
		self.lock = Lock()
		
		resting_p = (self.resting-self.minimum)/(self.maximum-self.minimum)
		self.phase = math.asin(resting_p*2-1)
		self.multiplier = self.frequency*2*math.pi
		self.stopped = True
		self.start_time = None
		self.killed = False
	
	def dance(self):
		with self.lock:
			for i in range(2):
				self.servo.value = -1
				time.sleep(0.5)
				self.servo.value = 1
				time.sleep(0.5)
			
			self.servo.value = self.resting
			time.sleep(self.servo_reset_delay)
			self.servo.value = None
			
	
	def kill(self):
		self.killed = True
		self.stop_moving()
	
	def start_moving(self):
		if self.start_time is None:
			self.start_time = time.time()
		self.stopped = False
	
	def stop_moving(self):
		with self.lock:
			self.stopped = True
			self.servo.value = self.resting
			time.sleep(self.servo_reset_delay)
			self.start_time = None
			self.servo.value=None
	
	def run(self):
		while not self.killed:
			with self.lock:
				if not self.stopped:
					t = time.time()-self.start_time
					a = (math.sin(t*self.multiplier+self.phase)+1)/2
					self.servo.value = a*(self.maximum-self.minimum)+self.minimum

if __name__ == "__main__":
	controller = ServoController()	

	controller.start()

	try:
		while True:
			i = input(">> ")
			if i == "0":
				controller.stop_moving()
			elif i == "1":
				controller.start_moving()
			elif i == "q":
				break
	finally:
		controller.kill()
