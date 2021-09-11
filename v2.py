#! /usr/bin/python3

import struct
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
		try:
			self.subprocess = subprocess.Popen(InjectionAPI.injector_filepath)

			time.sleep(0.5)
			if self.subprocess.poll() != None:
				print("Error polling subprocess.")
				return -1

			self.scan()
			self.poll()

		except OSError as err:
			print(err)

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


from module import Module
from module import ModuleController

from input import Input
from input import InputController

from output import Output
from output import OutputController

# dearpygui Window
class InjectionUI():
	def __init__(self, input_controller, module_controller, output_controller, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		VIEWPORT_WIDTH = 800
		VIEWPORT_HEIGHT = 600
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

			for i, window in enumerate(("window_input", "window_module", "window_output")):
				dpg.set_item_pos(item=window, pos=((viewport_width/3) * i, 20))
				dpg.set_item_width(item=window, width=viewport_width/3)
				dpg.set_item_height(item=window, height=viewport_height)
		dpg.set_viewport_resize_callback(resize_viewport)

		dpg.set_primary_window("main_window", True)

		self.create_inputs_ui(input_controller)
		self.create_modules_ui(module_controller)
		self.create_outputs_ui(output_controller)

	def create_inputs_ui(self, input_controller):
		for inp in input_controller.get_inputs():
			with dpg.group(parent="window_input", horizontal=True):
				dpg.add_button(label=str(inp))
				# with dpg.tooltip(parent=dpg.last_item()):
				# 	dpg.add_text("LOT OF DATA HERE")
				with dpg.drag_payload(parent=dpg.last_item(), drag_data=inp, payload_type="data"):
					dpg.add_text(str(inp))
				dpg.add_checkbox(label="", user_data=inp, callback=lambda id, value, udata : udata.switch(), default_value=False)

	def create_modules_ui(self, module_controller):
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

						dpg.add_button(label=key)
						with dpg.drag_payload(parent=dpg.last_item(), drag_data=(key, out), payload_type="data"):
							dpg.add_text(key)

						dpg.add_text("0.0")
						dpg.add_visible_handler(parent=id,
							user_data=(dpg.last_item(), key, module),
							callback=lambda id, _, data: dpg.set_value(data[0], data[2]._outputs[data[1]].get_value() ))
							# callback=lambda id, _, data: dpg.set_value(data[0], data[2]._outputs[data[1]]))

	def create_outputs_ui(self, output_controller):
		#TODO: replace this by a button to add them dynamically
		for i in range(4):
			output = Output()
			output_controller.outputs.append(output)

		for output in output_controller.outputs:
			with dpg.group(parent="window_output", horizontal=True):

				def callback(id, data):
					out = dpg.get_item_user_data(id)
					key, module_output = data

					dpg.set_item_label(id, key)
					out.input = module_output

				dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
					user_data=output,
					drop_callback=callback)

				def callback2(id, _, user_data):
					id_but, out = user_data
					if out:
						dpg.set_value(id_but, out.get_value())

				dpg.add_text("0.0")
				dpg.add_visible_handler(parent=dpg.last_item(),
					user_data=(dpg.last_item(), output),
					callback=callback2)

				dpg.add_input_int(default_value=0, width=100, min_value=0, max_value=255, step=1)

	def update(self):
		dpg.render_dearpygui_frame()

# MAIN CLASS
class InjectionApp:
	def __init__(self):
		self.input_controller = InputController()
		self.module_controller = ModuleController()
		self.output_controller = OutputController()

		# pygame.init()
		# pygame.joystick.init()

		self.injectionAPI = InjectionAPI()
		self.injectionUI = None

	def initialize(self):
		# self.injectionAPI.start()
		# self.input_controller.scan_joysticks()
		# self.input_controller.init_inputs()

		self.module_controller.create_modules_dynamically()

		self.injectionUI = InjectionUI(self.input_controller, self.module_controller, self.output_controller)

	def run(self):
		while dpg.is_dearpygui_running():
			self.injectionUI.update()

			self.input_controller.update()
			self.module_controller.compute()

			# self.output_controller.update()
			# self.output_controller.send_outputs(self.injectionAPI, self.module_controller)

			time.sleep(1 / 40)

		dpg.cleanup_dearpygui()


def main():
	app = InjectionApp()
	app.initialize()
	app.run()

if __name__ == '__main__':
	main()

"""
WINDOWS 10: problems to fix
	- viewport not calling resize callback on start
	- pygame completely breaking the program
"""
