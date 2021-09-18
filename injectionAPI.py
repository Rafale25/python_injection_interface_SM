import struct
import time
import socket
import subprocess
import atexit

class InjectionAPI:
	injector_filepath = "C:/Program Files (x86)/Steam/steamapps/workshop/content/387990/1771470800/sminject.exe"

	def __init__(self):
		self.subprocess = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
		self.address = ('127.0.0.1', 25752)

		self.socket.settimeout(1) #1 second timeout

	def start(self):
		try:
			self.subprocess = subprocess.Popen(InjectionAPI.injector_filepath)

			time.sleep(0.5)
			if self.subprocess.poll() != None: #subprocess return None if alive
				print("Error polling subprocess.")
				return -1

			self.scan()
			self.poll()

			atexit.register(self.cleanup)

		except OSError as err:
			print(err)

	def cleanup(self):

		if self.subprocess and self.subprocess.poll() == None:
			self.subprocess.kill()

	def scan(self):
		self.socket.sendto(struct.pack(">B", 0x03), self.address)

	def poll(self):
		self.socket.sendto(struct.pack(">B", 0x04), self.address)

	def set_value(self, id, value):
		packet = bytearray(b'\x01')
		packet.extend(struct.pack(">Id", id, value))
		self.socket.sendto(packet, self.address)

	# def ask_value(self, id):
	# 	packet = bytearray(b'\x02')
	# 	packet.extend(struct.pack(">I", id))
	# 	self.socket.sendto(packet, self.address)
	#
	# def recv_value(self):
	# 	# header = self.socket.recv(2)
	# 	data = self.socket.recv(128)
	# 	print("packet data: {}".format(data))
	#
	# def get_value(self, id):
	# 	self.ask_value(id)
	# 	time.sleep(0.01)
	# 	self.recv_value()
