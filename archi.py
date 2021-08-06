import struct
import socket
import subprocess
import time

import importlib
import os

import tkinter as tk
from tkinter import ttk

from functools import partial

import pygame

from widgets import InputWidget, ModuleWidget, OutputWidget

# def cast_to_type(value, type):
# 	if type == 'float': return float(value)
# 	if type == 'int': return int(value)
# 	if type == 'tuple': return tuple(value)
# 	return value

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
	# INPUT_TYPE = {
	# 	'numball': 'float',
	# 	'axis': 'float',
	# 	'button': 'int',
	# 	'hat': 'tuple',
	# }

	def __init__(self, joystick, id, input_type):
		self.joystick = joystick
		self.id = id

		self.input_type = input_type
		self.value = 0
		self.check_box = tk.IntVar()

	def __str__(self):
		return "{} {}".format(self.input_type, self.id)

	def update(self):
		new_value = 0

		if self.input_type == 'numball':
			new_value = self.joystick.get_ball(self.id)
		elif self.input_type == 'axis':
			new_value = self.joystick.get_axis(self.id)
		elif self.input_type == 'button':
			new_value = self.joystick.get_button(self.id)
		elif self.input_type == 'hat':
			new_value = self.joystick.get_hat(self.id)

		# self.value = cast_to_type(new_value, Input.INPUT_TYPE[self.input_type])
		self.value = new_value

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
				inp = Input(joystick=joystick, id=i, input_type="numball")
				self.inputs.append(inp)
			for i in range(joystick.get_numaxes()):
				inp = Input(joystick=joystick, id=i, input_type="axis")
				self.inputs.append(inp)
			for i in range(joystick.get_numbuttons()):
				inp = Input(joystick=joystick, id=i, input_type="button")
				self.inputs.append(inp)
			for i in range(joystick.get_numhats()):
				inp = Input(joystick=joystick, id=i, input_type="hat")
				self.inputs.append(inp)

	def get_inputs(self):
		return self.inputs

	def update(self):
		for inp in self.inputs:
			inp.update()


# MODULES --
class Module:
	def __init__(self):
		self._name = None
		self._inputs = dict() #{string, Input}
		self._outputs = dict() #{string, value}

	def set_name(self, str):
		self._name = str

	def get_name(self):
		return self._name

	def get_inputs(self):
		return self._inputs

	def add_input(self, key):
		self._inputs[key] = None

	def get_input(self, key):
		return self._inputs[key]

	def get_outputs(self):
		return self._outputs

	def add_output(self, key):
		self._outputs[key] = 0

	def set_output(self, key, value):
		self._outputs[key] = value

	def compute(self):
		pass

class ModuleController:
	MODULE_FOLDER_PATH = "./modules"

	def __init__(self):
		# self.modules = dict() #{string, Module}
		self.modules_classes = []
		self.module_instances = []

	def get_modules(self):
		return self.module_instances

	def create_modules_dynamically(self):
		# import class dynamically and instantiate them
		modules_names = [path.split('.')[0] for path in os.listdir(ModuleController.MODULE_FOLDER_PATH) if path[-2:] == "py"]

		for name in modules_names:
			module = importlib.import_module("modules.{}".format(name))
			ModuleClass = getattr(module, name)
			self.modules_classes.append(ModuleClass)

		# TODO: Remove later
		# create an instance of every class/module
		for ModuleCLass in self.modules_classes:
			self.module_instances.append( ModuleCLass() )

	def compute(self):
		for module in self.modules:
			module.compute()


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
	WIDTH = 100
	BORDER_WIDTH = 3
	PADX = 10

	COLUMN_SIZE = WIDTH + BORDER_WIDTH + PADX

	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.minsize(InjectionUI.COLUMN_SIZE*3, 100)
		self.maxsize(1920, 1080)

		self.main_frame = tk.Frame(self, borderwidth=5, relief="raised")
		self.main_frame.pack(expand=True, fill="both")

		self.frame_inputs = tk.Frame(self.main_frame, borderwidth=InjectionUI.BORDER_WIDTH, padx=InjectionUI.PADX, relief="raised")
		self.frame_modules = tk.Frame(self.main_frame, borderwidth=InjectionUI.BORDER_WIDTH, padx=InjectionUI.PADX, relief="raised")
		self.frame_outputs = tk.Frame(self.main_frame, borderwidth=InjectionUI.BORDER_WIDTH, padx=InjectionUI.PADX, relief="raised")

		self.frame_inputs.grid(row=0, column=0, sticky="NESW")
		self.frame_modules.grid(row=0, column=1, sticky="NESW")
		self.frame_outputs.grid(row=0, column=2, sticky="NESW")

		# give minimul width to columns
		for i in range(3):
			self.main_frame.grid_columnconfigure(i, minsize=InjectionUI.WIDTH, weight=1)

		self.tk_inputs = []
		self.tk_modules = []
		self.tk_outputs = []

	def create_inputs_ui(self, input_controller):
		for inp in input_controller.get_inputs():
			widget = InputWidget("{} {}".format(inp.input_type, inp.id), inp.check_box, self.frame_inputs)
			widget.pack()

			self.tk_inputs.append(widget)

	def create_modules_ui(self, input_controller, module_controller):
		for module in module_controller.get_modules():
			widget = ModuleWidget(module, input_controller.get_inputs(), self.frame_modules)
			widget.pack()

			self.tk_modules.append(widget)

	def create_outputs_ui(self, output_controller):
		pass

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

		self.module_controller.create_modules_dynamically()

		self.injectionUI.create_inputs_ui(self.input_controller)
		self.injectionUI.create_modules_ui(self.input_controller, self.module_controller)

	def run(self):
		while True:
			self.injectionUI.update_tk()
			time.sleep(1/40)


def main():
	app = InjectionApp()
	app.initialize()
	app.run()

if __name__ == '__main__':
	main()
