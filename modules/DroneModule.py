from archi import Module

class DroneModule(Module):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.inputs = dict({
			'thrust': 'float',
			'roll': 'float',
			'pitch': 'float',
			'yaw': 'float',
		})

	def compute(self):
		return 42
