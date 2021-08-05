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
		self.check_box = tk.IntVar()

	def __str__(self):
		return "{} {}".format(self.type, self.id)

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

		self.joystick_count = 0
		self.joysticks = []

	def scan_joysticks(self):
		self.joystick_count = pygame.joystick.get_count()
		self.joysticks = [pygame.joystick.Joystick(i) for i in range(self.joystick_count)]

	def init_inputs(self):
		for joystick in self.joysticks:
			for i in range(joystick.get_numballs()):
				inp = Input(joystick=joystick, id=i, type="numball")
				self.inputs.append(inp)
			for i in range(joystick.get_numaxes()):
				inp = Input(joystick=joystick, id=i, type="axis")
				self.inputs.append(inp)
			for i in range(joystick.get_numbuttons()):
				inp = Input(joystick=joystick, id=i, type="button")
				self.inputs.append(inp)
			for i in range(joystick.get_numhats()):
				inp = Input(joystick=joystick, id=i, type="hat")
				self.inputs.append(inp)

	def update(self):
		for inp in self.inputs:
			inp.update()


# MODULES --
class Module:
	def __init__(self):
		self.name = None
		self.inputs = dict() #{string, Input}

	def compute(self): # -> dict({string, value})
		pass

	def get_scheme(self): # -> list[string]
		pass

# class ModuleWidget(tk.Frame):
# 	def __init__(self, module, *args, **kwaargs):
# 		super().__init__(*args, **kwaargs)
#
# 		self.module = module
#
# 		self.frame_inputs = tk.Frame() # OptionMenu
# 		self.frame_outputs = tk.Frame() # Labels


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

		self.main_frame = tk.Frame(self, borderwidth=5, relief="raised")
		self.main_frame.pack(expand=True, fill="both")

		self.frame_inputs = tk.Frame(self.main_frame, borderwidth=5, relief="raised")
		self.frame_modules = tk.Frame(self.main_frame, borderwidth=5, relief="raised")
		self.frame_outputs = tk.Frame(self.main_frame, borderwidth=5, relief="raised")

		self.frame_inputs.grid(row=0, column=0)
		self.frame_modules.grid(row=0, column=1)
		self.frame_outputs.grid(row=0, column=2)

		self.tk_inputs = []
		# self.tk_modules = []
		# self.tk_outputs = []

	def create_inputs_ui(self, input_controller):
		tmp = []

		for inp in input_controller.inputs:

			line = tk.Checkbutton(self.frame_inputs, text=str(inp), variable=inp.check_box)
			line.pack()
			tmp.append(line)

		self.tk_inputs = tmp

		# for i in range(4):
		# 	e = tk.Label(self.frame_inputs, text="input {}".format(i))
		# 	e.pack()

	def update_tk(self):
		self.update_idletasks()
		self.update()

# MAIN CLASS
class InjectionApp:
	def __init__(self):
		self.input_controller = InputController()
		self.module_controller = ModuleController()
		self.output_controller = OutputController()

		self.injectionAPI = InjectionAPI()
		self.injectionUI = InjectionUI()

		pygame.init()
		pygame.joystick.init()

	def initialize(self):
		self.input_controller.scan_joysticks()
		self.input_controller.init_inputs()
		self.injectionUI.create_inputs_ui(self.input_controller)

	def run(self):
		while True:
			self.injectionUI.update_tk()
			time.sleep(1/40)


def main():
	app = InjectionApp()
	app.initialize()
	app.run()

if __name__ == '__main__':
	# main()



	# code to import class dynamcly and instantiate them
	import importlib
	import os

	modules_names = [path.split('.')[0] for path in os.listdir("./modules") if path[-2:] == "py"]
	modules_classes = []

	for name in modules_names:
		module = importlib.import_module("modules.{}".format(name))
		ModuleClass = getattr(module, name)
		modules_classes.append(ModuleClass)

	print(modules_classes)

	droneModule = modules_classes[0]()
	print( droneModule.compute() )

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
