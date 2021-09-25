import dearpygui.dearpygui as dpg

# drag_payload
class Var:
	# ID = 0

	def __init__(self, value=0.0, name="var"):
		self._value = value
		self._name = name

		# self.set_name("var {}".format(Var.ID))
		# Var.ID += 1

	def get_value(self):
		return self._value

	def get_name(self):
		return self._name

	def set_value(self, value):
		self._value = value

	def set_name(self, name):
		self._name = name

	# def __delete__(self):
		# dpg.delete_item(id)
