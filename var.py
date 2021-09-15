# drag_payload
class Var:
	def __init__(self, value):
		self._value = value

	def __str__(self):
		return "{}".format(self._value)

	def get_value(self):
		return self._value

	def set_value(self, value):
		self._value = value
