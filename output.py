class Output:
	def __init__(self):
		self._input = None # FloatVar
		self._input_key = ""
		self._id = 0
		self._checkbox = False

	def switch(self):
		self._checkbox = not self._checkbox

	def get_value(self):
		if self._input:
			return self._input.get_value()
		return 0.0

	def set_id(self, id):
		self._id = id

	def get_id(self):
		return self._id

class OutputController:
	def __init__(self):
		self.outputs = [] #[Output]

	def add_output(self):
		output = Output()
		self.outputs.append(output)
		return output

	def send_outputs(self, injectionAPI):
		for output in self.outputs:
			if not output._checkbox: continue
			if output._input:
				value = output._input.get_value()
				if value != None:
					injectionAPI.set_value(output.get_id(), value)
