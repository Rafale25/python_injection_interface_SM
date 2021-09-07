#! /usr/bin/python3

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
		self._joystick = joystick
		self._id = id

		self._input_type = input_type
		self._value = 0
		self._check_box = tk.IntVar()

	def __str__(self):
		return "{} {}".format(self._input_type, self._id)

	def is_on(self):
		return self._check_box.get()

	def get_value(self):
		return self._value

	def update(self):
		new_value = 0

		if self._input_type == 'numball':
			new_value = self._joystick.get_ball(self._id)
		elif self._input_type == 'axis':
			new_value = self._joystick.get_axis(self._id)
		elif self._input_type == 'button':
			new_value = self._joystick.get_button(self._id)
		elif self._input_type == 'hat':
			new_value = self._joystick.get_hat(self._id)

		new_value = 69
		self._value = new_value

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

	def get_inputs_name_id(self):
		return [str(inp) for inp in self.inputs]

	def update(self):
		for inp in self.inputs:
			if inp.is_on():
				inp.update()
			else:
				inp.value = 0

# MODULES --
class Module:
	def __init__(self):
		self._name = ""
		self._inputs = dict() #{key: Input}
		self._outputs = dict() #{key: DoubleVar}

	def set_name(self, str):
		self._name = str

	def get_name(self):
		return self._name

	def get_outputs_keys(self):
		return [key for key, value in self._outputs.items()]

	def get_outputs(self):
		return self._outputs

	def get_inputs_dict(self):
		return self._inputs

	def add_input(self, key):
		self._inputs[key] = None

	def get_input(self, key):
		if self._inputs[key] != None:
			return self._inputs[key].get_value()
		return None

	def get_outputs_dict(self):
		return self._outputs

	def add_output(self, key):
		self._outputs[key] = tk.DoubleVar()
		self._outputs[key].set(0)

	def set_output(self, key, value):
		self._outputs[key].set(value)

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

	def get_outputs_items(self):
		items = {}
		for module in self.module_instances:
			items.update(module.get_outputs())
		return items

	def get_outputs_keys(self):
		keys = []
		for module in self.module_instances:
			keys.extend(module.get_outputs_keys())
		return keys

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
		for module in self.module_instances:
			module.compute()

# OUTPUTS --
class Output:
	def __init__(self):
		self.input = None
		self.input_key = tk.StringVar() #key from module
		self.id = tk.IntVar()
		self.id.set(0)

	def get_value(self, module_controller):
		module_output_name = self.input_key.get()
		for m_instance in module_controller.module_instances:
			if module_output_name in m_instance._outputs.keys():
				return m_instance._outputs[module_output_name].get()
		return None

	def get_id(self):
		return self.id.get()

class OutputController:
	def __init__(self):
		# self.outputs = dict() # dict({string, Output})
		self.outputs = [] # [Output]

	def add_output(self):
		pass

	def send_outputs(self, injectionAPI, module_controller):
		print(self.outputs[0].get_value(module_controller))

		for output in self.outputs:
			if output.input_key.get():
				injectionAPI.set_value(output.get_id(), output.get_value(module_controller))


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

		self.main_frame = tk.Frame(self, borderwidth=0, relief="raised")
		self.main_frame.pack(expand=True, fill="both")

		self.frame_inputs = tk.Frame(self.main_frame, borderwidth=InjectionUI.BORDER_WIDTH, padx=InjectionUI.PADX, relief="raised")
		self.frame_modules = tk.Frame(self.main_frame, borderwidth=InjectionUI.BORDER_WIDTH, padx=InjectionUI.PADX, relief="raised")
		self.frame_outputs = tk.Frame(self.main_frame, borderwidth=InjectionUI.BORDER_WIDTH, padx=InjectionUI.PADX, relief="raised")

		self.frame_inputs.grid(row=0, column=0, sticky="NESW")
		self.frame_modules.grid(row=0, column=1, sticky="NESW")
		self.frame_outputs.grid(row=0, column=2, sticky="NESW")

		# give minimum width to columns
		for i in range(3):
			self.main_frame.grid_columnconfigure(i, minsize=InjectionUI.WIDTH, weight=1)

		self.tk_inputs = []
		self.tk_modules = []
		self.tk_outputs = []

	def create_inputs_ui(self, input_controller):
		for inp in input_controller.get_inputs():
			widget = InputWidget("{} {}".format(inp._input_type, inp._id), inp._check_box, self.frame_inputs)
			widget.pack()

			self.tk_inputs.append(widget)

	def create_modules_ui(self, input_controller, module_controller):
		for module in module_controller.get_modules():
			widget = ModuleWidget(module, input_controller, self.frame_modules)
			widget.pack(fill='x')

			self.tk_modules.append(widget)

	def create_outputs_ui(self, module_controller, output_controller):
		#TODO: replace this by a button to add them dynamically
		for i in range(4):
			output = Output()
			output_controller.outputs.append(output)

		modules_outputs = module_controller.get_outputs_keys()
		for output in output_controller.outputs:
			widget = OutputWidget(output, modules_outputs, self.frame_outputs)
			widget.pack()

			self.tk_outputs.append(widget)


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
		self.injectionAPI.start()
		self.input_controller.scan_joysticks()
		self.input_controller.init_inputs()

		self.module_controller.create_modules_dynamically()

		self.injectionUI.create_inputs_ui(self.input_controller)
		self.injectionUI.create_modules_ui(self.input_controller, self.module_controller)
		self.injectionUI.create_outputs_ui(self.module_controller, self.output_controller)

	def run(self):
		while True:
			self.injectionUI.update_tk()

			self.input_controller.update()
			self.module_controller.compute()
			# self.output_controller.update()
			self.output_controller.send_outputs(self.injectionAPI, self.module_controller)

			time.sleep(1/40)


def main():
	app = InjectionApp()
	app.initialize()
	app.run()

if __name__ == '__main__':
	main()


"""
##lists##
inputs []
module_outputs []

##commands##
checkForController
loadModule
link inputs/module_ouput to module_input/output

"""
