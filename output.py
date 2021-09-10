class Output:
	def __init__(self):
		self.input = None # Var
		self.input_key = ""
		self.id = 0

	def get_value(self):
		if self.input:
			return self.input.get_value()
		return 0.0

	def get_id(self):
		return self.id.get()

class OutputController:
	def __init__(self):
		self.outputs = [] #[Output]

	def add_output(self):
		pass

	def send_outputs(self, injectionAPI, module_controller):
		for output in self.outputs:
			if output.input_key.get():
				value = output.get_value(module_controller)
				if value != None:
					injectionAPI.set_value(output.get_id(), value)
