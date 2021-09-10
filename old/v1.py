#! /usr/bin/python3

import struct
import socket
import subprocess
import time

import tkinter as tk
from tkinter import ttk

from functools import partial

import pygame

def map_range(value, min1, max1, min2, max2):
	return min2 + (value - min1) * (max2 - min2) / (max1 - min1)

def clamp(value, min, max):
	if value < min: return min
	if value > max: return max
	return value

class InjectionAPI():
	injector_filepath = "C:/Program Files (x86)/Steam/steamapps/workshop/content/387990/1771470800/sminject.exe"

	def __init__(self):
		self.subprocess = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
		self.address = ('127.0.0.1', 25752)

	def __str__(self):
		pass

	def start(self):
		self.subprocess = subprocess.Popen(InjectionAPI.injector_filepath)

		time.sleep(0.5)
		if self.subprocess.poll() != None:
			return

		self.socket.settimeout(1)
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

class Input:
	def __init__(self, parent, joystick, type, id):
		self.frame = tk.Frame(parent, bd=2)
		self.frame.pack()

		self.joystick = joystick
		self.type = type
		self.id = id
		self.value = 0 # input balue updated

		self.var_peer_id = tk.IntVar()
		self.var_peer_id.set(0)
		self.var_on = tk.IntVar()
		self.var_on.set(0)
		self.var_displaytext = tk.StringVar()
		self.var_displaytext.set('0')

		self.title = tk.Label(self.frame, text="{} {}".format(self.type, self.id))
		self.check_box = tk.Checkbutton(self.frame, variable=self.var_on, onvalue=1, offvalue=0)
		self.peer_id = ttk.Spinbox(
			self.frame,
			from_=0,
			to=16,
			textvariable=self.var_peer_id,
			wrap=True,
			width=4)
		self.display_value = tk.Label(self.frame, textvariable=self.var_displaytext)

		self.title.grid(row=0, column=0)
		self.peer_id.grid(row=0, column=1)
		self.check_box.grid(row=0, column=2)
		self.display_value.grid(row=0, column=3)

		if type in ('axis', 'numball'):
			# map_range
			self.var_min1 = tk.DoubleVar()
			self.var_max1 = tk.DoubleVar()
			self.var_min2 = tk.DoubleVar()
			self.var_max2 = tk.DoubleVar()

			self.var_min1.set(-1)
			self.var_max1.set(1)
			self.var_min2.set(-1)
			self.var_max2.set(1)

			self.entry_min1 = tk.Entry(self.frame, textvariable=self.var_min1, width=10)
			self.entry_max1 = tk.Entry(self.frame, textvariable=self.var_max1, width=10)
			self.entry_min2 = tk.Entry(self.frame, textvariable=self.var_min2, width=10)
			self.entry_max2 = tk.Entry(self.frame, textvariable=self.var_max2, width=10)

			self.entry_min1.grid(row=0, column=4)
			self.entry_max1.grid(row=0, column=5)
			self.entry_min2.grid(row=0, column=6)
			self.entry_max2.grid(row=0, column=7)

	def update(self):
		new_value = 0

		if self.type == 'numball':
			new_value = self.joystick.get_ball(self.id)
			self.var_displaytext.set("{:.3f}".format(self.value))
		if self.type == 'axis':
			new_value = self.joystick.get_axis(self.id)
			self.var_displaytext.set("{:.3f}".format(self.value))
		if self.type == 'button':
			new_value = self.joystick.get_button(self.id)
			self.var_displaytext.set("{}".format(self.value))
		if self.type == 'hat':
			new_value = self.joystick.get_hat(self.id)
			self.var_displaytext.set("{}".format(self.value))

		self.value = new_value

	def get_value(self):
		if type in ('axis', 'numball'):
			return map_range(
				self.value,
				self.var_min1.get(),
				self.var_max1.get(),
				self.var_min2.get(),
				self.var_max2.get()
			)
		return self.value

	def get_peer_id(self):
		return self.var_peer_id.get()

	def is_on(self):
		return self.var_on.get() == 1

class InjectionUI:
	def __init__(self):
		self.window = tk.Tk()
		self.window.minsize(200, 100)

		self.api = InjectionAPI()
		self.api.start()

		pygame.init()
		pygame.joystick.init()
		self.joystick = pygame.joystick.Joystick(0)
		self.joystick.init()

		self.buttons_frame = tk.Frame()
		self.button_scan = tk.Button(self.buttons_frame, text="Scan", width=10, command=self.api.scan)
		self.button_poll = tk.Button(self.buttons_frame, text="Poll", width=10, command=self.api.poll)
		self.buttons_frame.pack(side=tk.TOP)
		self.button_scan.grid(row=0, column=0)
		self.button_poll.grid(row=0, column=1)

		self.inputs_name = []
		self.inputs = []
		self.inputs_frame = tk.Frame()
		self.inputs_frame.pack(side=tk.LEFT)

	def init_joystick_inputs(self):
		n = self.joystick.get_numballs()
		self.inputs_name.extend(f"trackball {i}" for i in range(n))

		n = self.joystick.get_numaxes()
		self.inputs_name.extend(f"axis {i}" for i in range(n))

		n = self.joystick.get_numbuttons()
		self.inputs_name.extend(f"button {i}" for i in range(n))

		n = self.joystick.get_numhats()
		self.inputs_name.extend(f"hat {i}" for i in range(n))

	def create_inputs_ui(self):
		for title in self.inputs_name:
			type, id = title.split(' ')
			inp = Input(parent=self.inputs_frame, joystick=self.joystick, type=type, id=int(id))
			self.inputs.append(inp)

	def update_inputs(self):
		for e in self.inputs:
			# if e.is_on():
			e.update()

	def transfer_values(self):
		for e in self.inputs:
			if e.is_on():
				self.api.set_value(e.get_peer_id(), e.get_value())

	def run(self):
		self.init_joystick_inputs()
		self.create_inputs_ui()

		while True:
			self.window.update_idletasks()
			self.window.update()

			pygame.event.pump()

			self.update_inputs()
			self.transfer_values()

			time.sleep(1 / 40)

def main():
	ui = InjectionUI()
	ui.run()

if __name__ == '__main__':
	main()
