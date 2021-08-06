from archi import Module

class ExampleModule(Module):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.set_name("Example Module")

		self.add_input('exampleInput')
		self.add_output("exampleOutput")

	def compute(self):
		input_value = self.get_input('exampleInput')

		# -- Do stuff here -- #

		self.set_output("exampleOutput", 42)
