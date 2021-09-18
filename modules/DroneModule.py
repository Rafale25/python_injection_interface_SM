from module import Module

class DroneModule(Module):
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		self.set_name("Drone Controller")

		self.add_input('thrust')
		self.add_input('roll')
		self.add_input('pitch')
		self.add_input('yaw')
		self.add_input('arm_sw')

		self.add_output("motorSE") # 1 (old 4)
		self.add_output("motorNE") # 2 (old 2)
		self.add_output("motorSW") # 3 (old 3)
		self.add_output("motorNW") # 4 (old 1)

	def compute(self):
		thrust = self.get_input('thrust')
		roll = self.get_input('roll')
		pitch = self.get_input('pitch')
		yaw = self.get_input('yaw')
		arm_sw = self.get_input('arm_sw')

		# Do stuff #
		max = 1764*6

		if arm_sw > 0 :
			#thrust :
			value = ((round(thrust, 3)) +1) * 3000
			motorNW = value
			motorNE = value
			motorSW = value
			motorSE = value

			#pitch :
			value = (round(pitch, 3)) * (-1000)
			if (motorNW + value <= max and motorNW + value >= -1000):
				motorNW += value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorNE += value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorSW -= value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorSE -= value

			#roll :
			value = (round(roll, 3)) * 1000
			if (motorNW + value <= max and motorNW + value >= -1000):
				motorNW += value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorNE -= value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorSW += value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorSE -= value

			#yaw :
			value = (round(yaw, 3)) * (-1000)
			if (motorNW + value <= max and motorNW + value >= -1000):
				motorNW += value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorNE -= value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorSW -= value
			if (motorNE + value <= max and motorNE + value >= -1000):
				motorSE += value
		else :
			motorNW = 0
			motorNE = 0
			motorSW = 0
			motorSE = 0

		self.set_output("motorNW", motorNW)
		self.set_output("motorNE", motorNE)
		self.set_output("motorSW", motorSW)
		self.set_output("motorSE", motorSE)
