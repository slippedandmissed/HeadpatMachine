from threading import Thread
from gpiozero import Button

class OverrideController(Thread):
	def __init__(self, queue, pin=23):
		Thread.__init__(self)
		self.queue = queue
		self.button = Button(pin)
		self.killed = False
	
	def kill(self):
		self.killed = True
	
	def run(self):
		while not self.killed:
			queue.override = self.button.is_pressed
		
