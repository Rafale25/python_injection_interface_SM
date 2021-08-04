import struct
import socket
import subprocess
import time

import tkinter as tk
from tkinter import ttk

from functools import partial

import pygame

# injectionAPI
class InjectionAPI:
	injector_filepath = "C:/Program Files (x86)/Steam/steamapps/workshop/content/387990/1771470800/sminject.exe"

	def __init__(self):
		self.subprocess = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
		self.address = ('127.0.0.1', 25752)

		self.socket.settimeout(1)

	def __str__(self):
		pass

	def start(self):
		self.subprocess = subprocess.Popen(InjectionAPI.injector_filepath)

		time.sleep(0.5)
		if self.subprocess.poll() != None:
			print("Error polling subprocess.")
			return -1

		self.scan()
		self.poll()

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


# INPUTS --
class Input:
	INPUT_TYPE = {
		'numball': float,
		'axis': float,
		'button': int,
		'hat': tuple,
	}

	def __init__(self, joystick, id, type):
		self.joystick = joystick
		self.id = id

		self.type = type
		self.value = 0

	def update(self):
		new_value = 0

		if self.type == 'numball':
			new_value = self.joystick.get_ball(self.id)
		elif self.type == 'axis':
			new_value = self.joystick.get_axis(self.id)
		elif self.type == 'button':
			new_value = self.joystick.get_button(self.id)
		elif self.type == 'hat':
			new_value = self.joystick.get_hat(self.id)

		self.value = Input.INPUT_TYPE[self.type](new_value)

class InputController:
	def __init__(self):
		self.inputs = []

	def update(self):
		for inp in self.inputs:
			inp.update()


# MODULES --
class Module:
	def __init__(self):
		self.inputs = dict() #{string, Input}

	def compute(self): # -> dict({string, value})
		pass

	def get_scheme(self): # -> list[string]
		pass

class ModuleController:
	def __init__(self):
		self.modules = dict() #{string, Module}

	def compute(self):
		pass


# OUTPUTS --
class Output:
	def __init__(self):
		self.inputs = dict() #{string}
		pass

class OutputController:
	def __init__(self):
		# self.injectionAPI = injectionAPI
		self.outputs = dict() # dict({string, Output})
		pass

	def send_outputs(self):
		pass


# tkinter Window
class InjectionUI(tk.Tk):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.minsize(200, 100)

		self.main_frame = tk.Frame(self, borderwidth= 5, relief="raised")
		self.main_frame.pack(expand=True, fill="both")

		self.frame_inputs = tk.Frame(self.main_frame, borderwidth=5, relief="raised")
		self.frame_modules = tk.Frame(self.main_frame, borderwidth=5, relief="raised")
		self.frame_outputs = tk.Frame(self.main_frame, borderwidth=5, relief="raised")

		self.frame_inputs.grid(row=0, column=0)
		self.frame_modules.grid(row=0, column=1)
		self.frame_outputs.grid(row=0, column=2)

		self.frame_inputs.grid_propagate(0)
		self.frame_modules.grid_propagate(0)
		self.frame_outputs.grid_propagate(0)

		for i in range(4):
			e = tk.Label(self.frame_inputs, text="input {}".format(i))
			e.pack()

		for i in range(4):
			e = tk.Label(self.frame_modules, text="module {}".format(i))
			e.pack()

		for i in range(4):
			e = tk.Label(self.frame_outputs, text="peer {}".format(i))
			e.pack()

	def update_tk(self):
		self.update_idletasks()
		self.update()

# MAIN CLASS
class InjectionApp:
	def __init__(self):
		self.injectionAPI = InjectionAPI()
		self.injectionUI = InjectionUI()

		self.input_controller = InputController()
		self.module_controller = ModuleController()
		self.output_controller = OutputController()

	def run(self):
		while True:
			self.injectionUI.update_tk()
			time.sleep(1/40)


def main():
	app = InjectionApp()
	app.run()

if __name__ == '__main__':
	main()

"""
Input:
	name check_box

Module:
	name
input0 output0
input1 output1
input2 output2

Output:
	peer_id
module output_name
"""
