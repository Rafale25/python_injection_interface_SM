#! /usr/bin/python3

import struct
import socket
import subprocess
import time

import importlib
import os

# import tkinter as tk
# from tkinter import ttk

# from functools import partial

import pygame
import dearpygui.dearpygui as dpg

# from widgets import InputWidget, ModuleWidget, OutputWidget

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
		self._check_box = False

	def __str__(self):
		return "{} {}".format(self._input_type, self._id)

	def is_on(self):
		return self._check_box

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

		# new_value = 69 #DEBUG
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


from module import Module
from module import ModuleController

# OUTPUTS --
class Output:
	def __init__(self):
		self.input = None
		self.input_key = tk.StringVar()
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
		for output in self.outputs:
			if output.input_key.get():
				value = output.get_value(module_controller)
				if value != None:
					injectionAPI.set_value(output.get_id(), value)


# tkinter Window
class InjectionUI():
	def __init__(self, input_controller, module_controller, output_controller, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		VIEWPORT_WIDTH = 600
		VIEWPORT_HEIGHT = 400
		VIEWPORT_MIN_WIDTH = 600
		VIEWPORT_MIN_HEIGHT = 200

		with dpg.window(id="main_window", menubar=True):
			pass
			with dpg.window(
				label="Input", id="window_input", no_move=True, no_collapse=True, no_close=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass

			with dpg.window(
				label="Module", id="window_module", no_move=True, no_collapse=True, no_close=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass

			with dpg.window(
				label="Output", id="window_output", no_move=True, no_collapse=True, no_close=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass


		dpg.setup_viewport()
		dpg.set_viewport_title(title="Sm Injector Interface")
		dpg.set_viewport_width(VIEWPORT_WIDTH)
		dpg.set_viewport_height(VIEWPORT_HEIGHT)
		dpg.set_viewport_min_width(VIEWPORT_MIN_WIDTH)
		dpg.set_viewport_min_height(VIEWPORT_MIN_HEIGHT)
		dpg.set_viewport_vsync(True)

		dpg.set_viewport_resizable(True)

		def resize_viewport(_, size):
			viewport_width = dpg.get_viewport_width()
			viewport_height = dpg.get_viewport_height()

			# for i, window in enumerate(("INPUT", "MODULE", "OUTPUT")):
			for i, window in enumerate(("window_input", "window_module", "window_output")):
				dpg.set_item_pos(item=window, pos=((viewport_width/3) * i, 20))
				dpg.set_item_width(item=window, width=viewport_width/3)
				dpg.set_item_height(item=window, height=viewport_height)
		dpg.set_viewport_resize_callback(resize_viewport)

		dpg.set_primary_window("main_window", True)

		self.create_inputs_ui(input_controller)
		# self.create_modules_ui(input_controller, module_controller)
		# self.create_outputs_ui(output_controller, output_controller)

	def create_inputs_ui(self, input_controller):
		for inp in input_controller.get_inputs():

			# with dpg.child(parent="window_input", autosize_x=True, autosize_y=True, width=0, height=0):
				# with dpg.tooltip(parent=dpg.last_item()):
				# 	dpg.add_text("LOT OF DATA HERE")
			dpg.add_button(parent="window_input", label=str(inp))
			with dpg.drag_payload(parent=dpg.last_item(), drag_data=inp, payload_type="data"):
				dpg.add_text(str(inp))
			dpg.add_same_line(parent="window_input")
			dpg.add_checkbox(parent="window_input", label="", callback=None, default_value=False)

	def create_modules_ui(self, input_controller, module_controller):
		# for module in module_controller.get_modules():
		pass

	def create_outputs_ui(self, module_controller, output_controller):
		#TODO: replace this by a button to add them dynamically
		# for i in range(4):
		# 	output = Output()
		# 	output_controller.outputs.append(output)

		# modules_outputs = module_controller.get_outputs_keys()
		# for output in output_controller.outputs:
		pass

	def update(self):
		dpg.render_dearpygui_frame()

# MAIN CLASS
class InjectionApp:
	def __init__(self):
		self.input_controller = InputController()
		self.module_controller = ModuleController()
		self.output_controller = OutputController()

		pygame.init()
		pygame.joystick.init()

		self.injectionAPI = InjectionAPI()
		self.injectionUI = None

	def initialize(self):
		# self.injectionAPI.start()
		self.input_controller.scan_joysticks()
		self.input_controller.init_inputs()

		self.injectionUI = InjectionUI(self.input_controller, self.module_controller, self.output_controller)

		self.module_controller.create_modules_dynamically()

		# self.injectionUI.create_inputs_ui(self.input_controller)
		# self.injectionUI.create_modules_ui(self.input_controller, self.module_controller)
		# self.injectionUI.create_outputs_ui(self.module_controller, self.output_controller)

	def run(self):
		while dpg.is_dearpygui_running():
		# while True:
			# self.injectionUI.update()
			dpg.render_dearpygui_frame()

			self.input_controller.update()
			self.module_controller.compute()
			# self.output_controller.update()
			# self.output_controller.send_outputs(self.injectionAPI, self.module_controller)

			time.sleep(1/40)

		dpg.cleanup_dearpygui()


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
