from servocontroller import ServoController
from threading import Thread, Lock
import time

class QueueController(Thread):
	def __init__(self, duration=4):
		Thread.__init__(self)
		self.duration = duration
		self.controller = ServoController()
		self.controller.start()
		self.start_time = None
		self.lock = Lock()
		self.moving = False
		self.killed = False
		self.override = False
	
	def kill(self):
		with self.lock:
			self.killed = True
			self.controller.kill()
	
	def enqueue(self):
		if not self.override:
			self.start_time = time.time()
	
	def run(self):
		while not self.killed:
			with self.lock:
				if not self.moving and (self.override or (self.start_time is not None and (time.time() - self.start_time < self.duration))):
					self.moving = True
					self.controller.start_moving()
				elif self.moving and not self.override and (self.start_time is None or (time.time()-self.start_time >= self.duration)):
					self.moving = False
					self.controller.stop_moving()
		
		

queue = QueueController()	

queue.start()

try:
	while True:
		i = input(">> ")
		if i == "0":
			queue.enqueue()
		elif i == "1":
			queue.override = not queue.override
		elif i == "q":
			break
finally:
	queue.kill()
