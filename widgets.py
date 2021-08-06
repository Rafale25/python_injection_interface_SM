import tkinter as tk
from tkinter import ttk

class InputWidget(tk.Frame):
	def __init__(self, name, intvar, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		# add variable type (float, int, tuple) in a way or another
		self.name = tk.Label(self, text=name)
		self.check_box = tk.Checkbutton(self, variable=intvar)

		self.name.grid(row=0, column=0)
		self.check_box.grid(row=0, column=1)


class ModuleWidget(tk.LabelFrame):
	def __init__(self, module, inputs, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		# self.module = module

		self['text'] = module.get_name()
		# self.label_name = tk.Label(self, text=module.get_name())
		# self.label_name.pack()

		self.frame_inputs = tk.Frame(self) # OptionMenu
		self.frame_outputs = tk.Frame(self) # Labels

		self.frame_inputs.grid(row=0, column=0)
		self.frame_outputs.grid(row=0, column=1)

		# self.input_options = dict() #{key, optionMenu}
		#
		# for key in module.get_inputs():
		# 	self.add_input_optionmenu(key, inputs)

	def add_input_optionmenu(self, key, inputs):

		list_options = (str(inp) for inp in inputs)
		var = tk.StringVar()
		# var.set(list_options[0])
		option_menu = tk.OptionMenu(self.frame_inputs, var, *list_options)
		option_menu.pack()
		self.input_options[key] = option_menu



class OutputWidget(tk.Frame):
	pass
