#! /usr/bin/python3

import dearpygui.dearpygui as dpg

class Var:
	def __init__(self, value=0.0, name="var"):
		self._value = value
		self._name = name

		dpg.set_staging_mode(True)
		self._value_source= dpg.add_string_value(default_value=str(value))
		self._name_source = dpg.add_string_value(default_value=name)
		dpg.set_staging_mode(False)

	def get_value(self):
		return self._value

	def get_name(self):
		return self._name

	def set_value(self, value):
		self._value = value

	def set_name(self, name):
		self._name = name
		dpg.set_value(self.get_name_source(), name)

	def get_value_source(self):
		return self._value_source

	def get_name_source(self):
		return self._name_source

var = Var(42.0, "myVar")

with dpg.window(id="main_window"):

	button = dpg.add_button(label=var.get_name(), width=100)
	with dpg.drag_payload(parent=button, drag_data=var, payload_type="data"):
		dpg.add_text(var.get_name())

	# add_mouse_release_handler
	dpg.add_same_line()
	dpg.add_button(label="edit", width=100)
	with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True) as modal:
		text_id = dpg.add_input_text(default_value="", width=300)

		def callback():
			new_name = dpg.get_value(text_id)
			var.set_name(new_name)

			dpg.set_item_label(button, new_name)
			dpg.configure_item(modal, show=False)
		dpg.add_button(label="apply", callback=callback)

	def callback(id, data, udata):
		text_value_id = dpg.get_item_user_data(id)
		dpg.set_item_source(id, data.get_name_source())
		dpg.set_item_source(text_value_id, data.get_value_source())

	text_value = dpg.add_text(default_value="0.0")
	dpg.add_same_line()
	dpg.add_input_text(default_value="", user_data=text_value, width=75, enabled=False, payload_type="data", drop_callback=callback)


dpg.set_primary_window("main_window", True)

dpg.start_dearpygui()
