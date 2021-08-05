import tkinter as tk
from tkinter import ttk

class InputWidget(tk.Frame):
	def __init__(self, name, intvar, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.name = tk.Label(self, text=name)
		self.check_box = tk.Checkbutton(self, variable=intvar)

		self.name.grid(row=0, column=0)
		self.check_box.grid(row=0, column=1)


class ModuleWidget(tk.Frame):
	def __init__(self, module, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.module = module

		self.frame_inputs = tk.Frame(self) # OptionMenu
		self.frame_outputs = tk.Frame(self) # Labels

		self.frame_inputs.grid(row=0, column=0)
		self.frame_outputs.grid(row=0, column=1)


		# for inp in self.module.inputs:

class OutputWidget(tk.Frame):
	pass
