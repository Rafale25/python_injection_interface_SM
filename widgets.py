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
	def __init__(self, module, input_controller, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.module = module
		self.input_controller = input_controller

		self['text'] = module.get_name()

		self.frame_inputs = tk.LabelFrame(self, text="In", labelanchor='n', bd=2) # OptionMenu
		self.frame_outputs = tk.LabelFrame(self, text="Out", labelanchor='n', bd=2) # Labels

		self.frame_inputs.grid(row=0, column=0, sticky="N")
		self.frame_outputs.grid(row=0, column=1, sticky="N")

		# self.input_options = dict() #{key, optionMenu}
		self.outputs = dict() #{key, value}

		for key in module.get_inputs_dict():
			self.add_input(key)

		for key, var in module.get_outputs_dict().items():
			self.add_output(key, var)

	def add_input(self, key):
		self.frame = tk.Frame(self.frame_inputs)
		self.frame.pack()

		name = tk.Label(self.frame, text=key)
		name.pack(side=tk.LEFT)

		self.var = tk.StringVar()
		self.option_menu = None

		self.create_optionMenu(self.input_controller.get_inputs_name_id())

		# self.input_options[key] = self.option_menu

	# update optionMenu list and link the module_input with the input selected
	def option_menu_event(self, input_name):
		self.create_optionMenu(self.input_controller.get_inputs_name_id())
		inp = next((inp for inp in self.input_controller.get_inputs() if str(inp) == input_name), None)
		if inp: self.module._inputs[key] = inp

	def create_optionMenu(self, entries):
		if self.option_menu:
			self.option_menu.destroy()
		self.option_menu = tk.OptionMenu(self.frame, self.var, *entries, command=self.option_menu_event)
		self.option_menu.pack(side=tk.RIGHT)

	def add_output(self, key, var):
		frame = tk.Frame(self.frame_outputs)
		name = tk.Label(frame, text=key)
		value = tk.Label(frame, textvariable=var)

		frame.pack()
		name.pack(side=tk.LEFT)
		value.pack(side=tk.RIGHT)

		self.outputs[key] = 0

class OutputWidget(tk.Frame):
	def __init__(self, output, modules_outputs, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.str_var = tk.StringVar()
		self.option_menu = tk.OptionMenu(self, self.str_var, *modules_outputs, command=None)
		self.option_menu.pack(side=tk.LEFT)

		self.peer_id = ttk.Spinbox(self, from_=0, to=32, textvariable=output.id, wrap=True, width=4)
		self.peer_id.pack(side=tk.RIGHT)
