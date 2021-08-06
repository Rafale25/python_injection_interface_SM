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

		self.module = module
		self.inputs_ref = inputs

		self['text'] = module.get_name()

		self.frame_inputs = tk.LabelFrame(self, text="In", labelanchor='n', bd=2) # OptionMenu
		self.frame_outputs = tk.LabelFrame(self, text="Out", labelanchor='n', bd=2) # Labels

		self.frame_inputs.grid(row=0, column=0, sticky="N")
		self.frame_outputs.grid(row=0, column=1, sticky="N")

		self.input_options = dict() #{key, optionMenu}
		self.outputs = dict() #{key, value}

		for key in module.get_inputs_dict():
			self.add_input(key, inputs)

		for key, var in module.get_outputs_dict().items():
			self.add_output(key, var)

	def add_input(self, key, inputs):
		frame = tk.Frame(self.frame_inputs)
		frame.pack()

		name = tk.Label(frame, text=key)
		name.pack(side=tk.LEFT)

		list_options = (str(inp) for inp in inputs)
		var = tk.StringVar()

		# temporary function
		def link_input(input_name):
			self.module._inputs[key] = next(inp for inp in self.inputs_ref if str(inp) == input_name)

		option_menu = tk.OptionMenu(frame, var, *list_options, command=link_input)
		option_menu.pack(side=tk.RIGHT)

		self.input_options[key] = option_menu

	def add_output(self, key, var):
		frame = tk.Frame(self.frame_outputs)
		frame.pack()

		name = tk.Label(frame, text=key)
		name.pack(side=tk.LEFT)

		value = tk.Label(frame, textvariable=var)
		value.pack(side=tk.RIGHT)

		self.outputs[key] = 0

class OutputWidget(tk.Frame):
	pass
