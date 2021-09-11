class Output:
	def __init__(self):
		self._input = None # FloatVar
		self._input_key = ""
		self._id = 0

	def get_value(self):
		if self._input:
			return self._input.get_value()
		return 0.0

	def get_id(self):
		return self._id

class OutputController:
	def __init__(self):
		self.outputs = [] #[Output]

	def add_output(self):
		pass

	def send_outputs(self, injectionAPI):
		for output in self.outputs:
			if output._input:
				value = output._input.get_value()
				if value != None:
					injectionAPI.set_value(output.get_id(), value)
