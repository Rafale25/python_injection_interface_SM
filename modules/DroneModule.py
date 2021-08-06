from archi import Module

class DroneModule(Module):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.set_name("Drone Controller")

		self.add_input('thrust')
		self.add_input('roll')
		self.add_input('pitch')
		self.add_input('yaw')

		self.add_output("motorNW")
		self.add_output("motorNE")
		self.add_output("motorSW")
		self.add_output("motorSE")

	def compute(self):
		thrust = self.get_input_value('thrust')
		roll = self.get_input_value('roll')
		pitch = self.get_input_value('pitch')
		yaw = self.get_input_value('yaw')

		self.set_output("motorNW", 42)
		self.set_output("motorNE", 69)
		self.set_output("motorSW", 13)
		self.set_output("motorSE", 34)
