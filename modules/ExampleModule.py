# import sys
# sys.path.append("..")

from module import Module

class ExampleModule(Module):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		## Set title name of the module
		self.set_name("Example Module")

		## Add a named input
		self.add_input('exampleInput')

		## Add an output
		self.add_output("exampleOutput")

	def compute(self):
		## get value from a set input
		input_value = self.get_input('exampleInput')

		# -- Do stuff here -- #

		## set value of output
		self.set_output("exampleOutput", input_value)
