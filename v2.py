#! /usr/bin/python3

# import struct
import socket
import subprocess
import time

from functools import partial

import importlib
import os

import pygame
import dearpygui.dearpygui as dpg

# import dearpygui.dearpygui as dpg
# from dearpygui.demo import show_demo
# show_demo()
# dpg.start_dearpygui()
# exit()

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


from module import Module
from module import ModuleController

from input import Input
from input import InputController


# OUTPUTS --
class Output:
	def __init__(self):
		self.input = None
		self.input_key = ""
		self.id = 0

	def get_value(self, module_controller):
		module_output_name = self.input_key
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
				label="Input", id="window_input", no_move=True, no_collapse=True, no_close=True, no_resize=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass

			with dpg.window(
				label="Module", id="window_module", no_move=True, no_collapse=True, no_close=True, no_resize=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass

			with dpg.window(
				label="Output", id="window_output", no_move=True, no_collapse=True, no_close=True, no_resize=True,
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
		self.create_modules_ui(input_controller, module_controller)
		self.create_outputs_ui(module_controller, output_controller)

	def create_inputs_ui(self, input_controller):
		for inp in input_controller.get_inputs():
			with dpg.group(parent="window_input", horizontal=True):
				dpg.add_button(label=str(inp))
				# with dpg.tooltip(parent=dpg.last_item()):
				# 	dpg.add_text("LOT OF DATA HERE")
				with dpg.drag_payload(parent=dpg.last_item(), drag_data=inp, payload_type="data"):
					dpg.add_text(str(inp))
				dpg.add_checkbox(label="", callback=lambda id, value : inp.switch(), default_value=False)

	def create_modules_ui(self, input_controller, module_controller):
		for module in module_controller.get_modules():

			with dpg.child(parent="window_module", height=200, border=True):
				# IN
				dpg.add_text("IN", bullet=True)
				for key, inp in module._inputs.items():
					with dpg.group(horizontal=True):

						def callback(id, data):
							input_key = dpg.get_item_user_data(id)

							if input_key in module._inputs:
								module._inputs[input_key] = data
							dpg.set_item_label(id, str(data))

						dpg.add_text(key)
						dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
							user_data=key, drop_callback=callback)

				# OUT
				dpg.add_text("OUT", bullet=True)
				for key, out in module._outputs.items():
					with dpg.group(horizontal=True):
						pass
						# print()
						# dpg.add_text(key)
						# dpg.add_text("a")
						# dpg.add_visible_handler(parent=dpg.last_item(), callback=lambda x: dpg.set_item_label(dpg.last_item(), 2))
						# dpg.add_visible_handler(parent=dpg.last_item(), callback=lambda x: print(module._outputs[key]))


	def create_outputs_ui(self, module_controller, output_controller):
		#TODO: replace this by a button to add them dynamically
		for i in range(4):
			output = Output()
			output_controller.outputs.append(output)

		for output in output_controller.outputs:
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

		self.module_controller.create_modules_dynamically()

		self.injectionUI = InjectionUI(self.input_controller, self.module_controller, self.output_controller)

	def run(self):
		while dpg.is_dearpygui_running():
			self.injectionUI.update()

			self.input_controller.update()
			self.module_controller.compute()

			# print(self.module_controller.module_instances[1]._inputs)
			# print(self.module_controller.module_instances[1]._outputs)
			# print()

			# self.output_controller.update()
			# self.output_controller.send_outputs(self.injectionAPI, self.module_controller)

			time.sleep(1/10)

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
