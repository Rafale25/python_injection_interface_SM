from module import Module

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
		thrust = self.get_input('thrust')
		roll = self.get_input('roll')
		pitch = self.get_input('pitch')
		yaw = self.get_input('yaw')

		# Do stuff #
		thrust = (thrust + 1) * 2

		self.set_output("motorNW", thrust)
		self.set_output("motorNE", roll)
		self.set_output("motorSW", pitch)
		self.set_output("motorSE", yaw)
