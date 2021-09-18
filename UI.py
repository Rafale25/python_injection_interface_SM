from module import Module
from module import ModuleController

from input import Input
from input import InputController

from output import Output
from output import OutputController

import dearpygui.dearpygui as dpg

from var import Var

class InjectionUI:
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

	def initialize(self, injectionAPI, input_controller, module_controller, output_controller):
		VIEWPORT_WIDTH = 900
		VIEWPORT_HEIGHT = 600
		VIEWPORT_MIN_WIDTH = 600
		VIEWPORT_MIN_HEIGHT = 200

		## themes ##
		with dpg.theme(id="theme_center_aligned", default_theme=True):
			dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, x=0.5, y=0.5, category=dpg.mvThemeCat_Core)

		with dpg.theme(id="theme_button_delete"):
			dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 140, 23), category=dpg.mvThemeCat_Core)


		with dpg.window(id="main_window", menubar=True):
			with dpg.menu_bar():
				dpg.add_menu_item(label="Scan", callback=lambda: injectionAPI.scan())
				dpg.add_menu_item(label="Poll", callback=lambda: injectionAPI.poll())

			with dpg.table(header_row=True, row_background=False,
				borders_innerH=False, borders_outerH=False,
				borders_innerV=True, borders_outerV=False, scrollY=False):

				dpg.add_table_column(label="Input")
				dpg.add_table_column(label="Module")
				dpg.add_table_column(label="Output")

				# for spacing under header_row
				for i in range(3*2):
					dpg.add_table_next_column()

				with dpg.child(label="Input", id="window_input", border=False):
					pass

				dpg.add_table_next_column()
				with dpg.child(label="Module", id="window_module", border=False):
					pass

				dpg.add_table_next_column()
				with dpg.child(label="Output", id="window_output", border=False):
					pass

		dpg.setup_viewport()
		dpg.set_viewport_title(title="SM Injector Interface")
		dpg.set_viewport_width(VIEWPORT_WIDTH)
		dpg.set_viewport_height(VIEWPORT_HEIGHT)
		dpg.set_viewport_min_width(VIEWPORT_MIN_WIDTH)
		dpg.set_viewport_min_height(VIEWPORT_MIN_HEIGHT)
		dpg.set_viewport_vsync(True)
		dpg.set_viewport_resizable(True)

		dpg.set_primary_window("main_window", True)

		## widgets ##
		self.create_inputs_ui(input_controller)
		self.create_modules_ui(module_controller)
		self.create_outputs_ui(output_controller)

	#NOTE: Payload of data are always a tuple with (string, Var)
	def create_inputs_ui(self, input_controller):

		# joystick input
		with dpg.collapsing_header(parent="window_input", label="Joystick", default_open=True):
			with dpg.table(header_row=True,
				borders_innerH=False, borders_outerH=False, borders_innerV=False, borders_outerV=False):

				dpg.add_table_column(label="", width_fixed=True)
				dpg.add_table_column(label="on/off", width_fixed=True)
				dpg.add_table_column(label="invert", width_fixed=True)
				dpg.add_table_column(label="value", width_fixed=False)

				for inp in input_controller.get_inputs():
					dpg.add_button(label=str(inp))
					# with dpg.tooltip(parent=dpg.last_item()):
					# 	dpg.add_text("LOT OF DATA HERE")
					with dpg.drag_payload(parent=dpg.last_item(), drag_data=(str(inp), inp.get_var()), payload_type="data"):
						dpg.add_text(str(inp))


					dpg.add_table_next_column()
					dpg.add_checkbox(label="", user_data=inp, callback=lambda id, value, udata : udata.switch(), default_value=False)
					dpg.add_table_next_column()
					dpg.add_checkbox(label="", user_data=inp, callback=lambda id, value, udata : udata.invert(), default_value=False)


					dpg.add_table_next_column()
					# visible value callback
					def callback(id, data, udata):
						text_id, inpp = udata
						dpg.set_value(text_id, "{:g}".format(inpp.get_value()))

					dpg.add_text("0")
					dpg.add_visible_handler(parent=dpg.last_item(),
						user_data=(dpg.last_item(), inp),
						callback=callback)

					dpg.add_table_next_column()

		# Scrap Mechanic injector ouput
		with dpg.collapsing_header(parent="window_input", label="SM Output", default_open=True):
			pass

	def create_modules_ui(self, module_controller):
		for module in module_controller.get_modules():

			with dpg.collapsing_header(parent="window_module", label=module.get_name(), default_open=True):

				dpg.add_text("IN", bullet=True) # IN

				with dpg.table(header_row=False,
					borders_innerH=False, borders_outerH=False, borders_innerV=False, borders_outerV=False):

					dpg.add_table_column(label="", width_fixed=True)
					dpg.add_table_column(label="", width_fixed=False)

					for key, inp in module._inputs.items():

						def drop_callback(id, data):
							input_key, mod = dpg.get_item_user_data(id)
							str, var = data #payload
							if input_key in mod._inputs:
								mod._inputs[input_key] = var
							dpg.set_item_label(id, str)

						dpg.add_text(key)
						dpg.add_table_next_column()
						dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
							user_data=(key, module), drop_callback=drop_callback)
						dpg.add_table_next_column()

				# OUT
				dpg.add_text("OUT", bullet=True)

				with dpg.table(header_row=False,
					borders_innerH=False, borders_outerH=False, borders_innerV=False, borders_outerV=False):

					dpg.add_table_column(width_fixed=True)
					dpg.add_table_column(width_fixed=False)

					for key, out in module._outputs.items():
						dpg.add_button(label=key)
						with dpg.drag_payload(parent=dpg.last_item(), drag_data=(key, out), payload_type="data"):
							dpg.add_text(key)

						dpg.add_table_next_column()
						dpg.add_text("0.0")
						dpg.add_visible_handler(parent=dpg.last_item(),
							user_data=(dpg.last_item(), key, module),
							callback=lambda id, _, data: dpg.set_value(data[0], "{:.3f}".format(data[2]._outputs[data[1]].get_value()) ))
						dpg.add_table_next_column()

				 # add spacing between modules
				dpg.add_dummy(height=20)
				dpg.add_separator()

	def add_output(self, output_controller, output=None):
		#create output if not provided
		if not output:
			output = output_controller.add_output()

		with dpg.table(parent="output_container", header_row=False,
			borders_innerH=False, borders_outerH=False, borders_innerV=False, borders_outerV=False) as output_widget:

			dpg.add_table_column(label="in", width_fixed=True)
			dpg.add_table_column(label="value", width_fixed=True)
			dpg.add_table_column(label="id", width_fixed=True)
			dpg.add_table_column(label="on/off", width_fixed=True)
			dpg.add_table_column(label="delete", width_fixed=True)

			def drop_callback(id, data):
				out_widget = dpg.get_item_user_data(id)
				key, out = data

				dpg.set_item_label(id, key)
				out_widget._input = out

			# payload input
			dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
				user_data=output,
				drop_callback=drop_callback)

			def callback(id, data, udata):
				id_but, out = udata
				if out:
					dpg.set_value(id_but, "{:.3f}".format(out.get_value()))

			dpg.add_table_next_column()
			dpg.add_text("0.0")
			dpg.add_visible_handler(parent=dpg.last_item(),
				user_data=(dpg.last_item(), output),
				callback=callback)

			dpg.add_table_next_column()
			dpg.add_input_int(default_value=0, width=75, min_value=0, max_value=255, step=1,
				user_data=output,
				callback=lambda id, data, udata: udata.set_id(data))

			dpg.add_table_next_column()
			dpg.add_checkbox(label="", user_data=output, callback=lambda id, value, udata : udata.switch(), default_value=False)

			def delete_callback(id, data, udata):
				out, out_widget = udata
				dpg.delete_item(out_widget)
				output_controller.outputs.remove(out)

			dpg.add_table_next_column()
			dpg.add_button(label="X", user_data=(output, output_widget), width=20, callback=delete_callback)
			dpg.set_item_theme(dpg.last_item(), "theme_button_delete") #themes are declared in initialize()

			dpg.add_table_next_column()

	def create_outputs_ui(self, output_controller):
		# outputs container (so the + button can stay at the bottom)
		with dpg.group(parent="window_output", id="output_container"):
			pass

		for output in output_controller.outputs:
			self.add_output(output_controller, output)

		# add output button
		dpg.add_button(parent="window_output", label="+", width=-1, height=20,
			callback=lambda: self.add_output(output_controller, None))

	def is_running(self):
		return dpg.is_dearpygui_running()

	def update(self):
		dpg.render_dearpygui_frame()

	def cleanup(self):
		dpg.cleanup_dearpygui()

"""
TODO:
	- center text
	- add padding to table

	- make output item look better
"""
