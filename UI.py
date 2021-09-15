from module import Module
from module import ModuleController

from input import Input
from input import InputController

from output import Output
from output import OutputController

import dearpygui.dearpygui as dpg

from var import Var

# class LayoutHelper:
# 	def __init__(self):
# 		self.table_id = dpg.add_table(header_row=False, policy=dpg.mvTable_SizingStretchProp)
# 		dpg.push_container_stack(self.table_id)
#
# 	def add_widget(self, uuid, percentage):
# 		dpg.add_table_column(init_width_or_weight=percentage/100.0, parent=self.table_id)
# 		dpg.add_table_next_column(parent=self.table_id)
# 		dpg.set_item_width(uuid, -1)
#
# 	def submit(self):
# 		dpg.pop_container_stack()

class InjectionUI:
	def __init__(self, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

	def initialize(self, injectionAPI, input_controller, module_controller, output_controller):
		VIEWPORT_WIDTH = 800
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

		with dpg.table(parent="window_input", header_row=False,
			borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, policy=dpg.mvTable_SizingStretchProp):

			# mytable = LayoutHelper()
			# mytable.add_widget(dpg.add_button(label="25%"), 25.0)
			# mytable.add_widget(dpg.add_button(label="75%"), 75.0)
			# mytable.submit()
			# dpg.add_table_column(width_fixed=True, init_width_or_weight=0.0)#width_fixed=True)#, no_clip=True, width_stretch=True)
			dpg.add_table_column(init_width_or_weight=1, width_stretch=True)#, no_clip=True, )
			dpg.add_table_column()
			dpg.add_table_column()
			dpg.add_table_column()

			for inp in input_controller.get_inputs():
				# with dpg.group(parent="window_input", horizontal=True):
				# with dpg.table(parent="window_input", header_row=False):

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


	def create_modules_ui(self, module_controller):
		for module in module_controller.get_modules():

			with dpg.collapsing_header(parent="window_module", label=module.get_name(), default_open=True):

				# IN
				dpg.add_text("IN", bullet=True)
				for key, inp in module._inputs.items():
					with dpg.group(horizontal=True):

						def drop_callback(id, data):
							input_key, mod = dpg.get_item_user_data(id)
							str, var = data #payload

							if input_key in mod._inputs:
								mod._inputs[input_key] = var
							dpg.set_item_label(id, str)

						dpg.add_text(key)
						dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
							user_data=(key, module), drop_callback=drop_callback)

				# OUT
				dpg.add_text("OUT", bullet=True)
				for key, out in module._outputs.items():
					with dpg.group(horizontal=True):

						dpg.add_button(label=key)
						with dpg.drag_payload(parent=dpg.last_item(), drag_data=(key, out), payload_type="data"):
							dpg.add_text(key)

						dpg.add_text("0.0")
						dpg.add_visible_handler(parent=dpg.last_item(),
							user_data=(dpg.last_item(), key, module),
							callback=lambda id, _, data: dpg.set_value(data[0], "{:.3f}".format(data[2]._outputs[data[1]].get_value()) ))

				dpg.add_dummy(height=10) # spacing
				dpg.add_separator()

	def add_output(self, output_controller, output=None):
		#create output if not provided
		if not output:
			output = output_controller.add_output()

		with dpg.group(parent="output_container", horizontal=False) as output_widget:

			with dpg.group(horizontal=True):
				def drop_callback(id, data):
					out_widget = dpg.get_item_user_data(id)
					key, out = data

					dpg.set_item_label(id, key)
					out_widget._input = out

				dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
					user_data=output,
					drop_callback=drop_callback)

				def callback(id, data, udata):
					id_but, out = udata
					if out:
						dpg.set_value(id_but, "{:.3f}".format(out.get_value()))

				dpg.add_text("=")
				dpg.add_text("0.0")
				dpg.add_visible_handler(parent=dpg.last_item(),
					user_data=(dpg.last_item(), output),
					callback=callback)

			with dpg.group(horizontal=True):

				dpg.add_input_int(default_value=0, width=100, min_value=0, max_value=255, step=1,
					user_data=output,
					callback=lambda id, data, udata: udata.set_id(data))
				dpg.add_checkbox(label="", user_data=output, callback=lambda id, value, udata : udata.switch(), default_value=False)

				def delete_callback(id, data, udata):
					out, out_widget = udata
					dpg.delete_item(out_widget)
					output_controller.outputs.remove(out)

				dpg.add_button(label="X", user_data=(output, output_widget), width=20, callback=delete_callback)
				dpg.set_item_theme(dpg.last_item(), "theme_button_delete") #themes are declared in initialize()

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

	- make input item look better
	- make output item look better
"""
