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

		# self.input_options = dict() #{key: (optionMenu, var)}
		self.outputs = dict() #{key, value}

		for key in module.get_inputs_dict():
			self.add_input(key)

		for key, var in module.get_outputs_dict().items():
			self.add_output(key, var)


	# update optionMenu list and link the module_input with the input selected
	def option_menu_event(self, key, module_input_name):
		# input_found = next((e for e in self.input_controller.get_inputs() if str(e) == key), None)
		if input_found := next((e for e in self.input_controller.get_inputs() if str(e) == key), None):
			self.module._inputs[module_input_name] = input_found

	def add_input(self, key):
		frame = tk.Frame(self.frame_inputs)
		title = tk.Label(frame, text=key)

		frame.pack()
		title.pack(side=tk.LEFT)

		var = tk.StringVar()

		inputs_name_id = self.input_controller.get_inputs_name_id()
		if not inputs_name_id:
			inputs_name_id = [""]

		option_menu = tk.OptionMenu(frame, var, *inputs_name_id, command=lambda x: self.option_menu_event(x, key))
		option_menu.pack(side=tk.RIGHT)

		# self.input_options[key] = option_menu

	def add_output(self, key, var):
		frame = tk.Frame(self.frame_outputs)
		title = tk.Label(frame, text=key)
		value = tk.Label(frame, textvariable=var)

		frame.pack()
		title.pack(side=tk.LEFT)
		value.pack(side=tk.RIGHT)

		self.outputs[key] = 0

class OutputWidget(tk.Frame):
	def __init__(self, output, modules_outputs, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.option_menu = tk.OptionMenu(self, output.input_key, *modules_outputs, command=None)
		self.option_menu.pack(side=tk.LEFT)

		self.peer_id = ttk.Spinbox(self, from_=0, to=32, textvariable=output.id, wrap=True, width=4)
		self.peer_id.pack(side=tk.RIGHT)
