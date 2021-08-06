from archi import Module

# set_name(string)
# add_input(string)
# add_output(string)
# get_input_value(string)
# set_output(string, value)

class ExampleModule(Module):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.set_name("Example")


	def compute(self):
		pass
