from archi import Module

class DroneModule(Module):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

	def compute(self):
		return 42
