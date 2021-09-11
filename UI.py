from module import Module
from module import ModuleController

from input import Input
from input import InputController

from output import Output
from output import OutputController

import dearpygui.dearpygui as dpg

class InjectionUI():
	def __init__(self, input_controller, module_controller, output_controller, *args, **kwaargs):
		super().__init__(*args, **kwaargs)

		VIEWPORT_WIDTH = 800
		VIEWPORT_HEIGHT = 600
		VIEWPORT_MIN_WIDTH = 600
		VIEWPORT_MIN_HEIGHT = 200

		with dpg.window(id="main_window", menubar=True):
			pass
			with dpg.window(
				label="Input", id="window_input", no_move=True, no_collapse=True, no_close=True, no_resize=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass

			with dpg.window(
				label="Module", id="window_module", no_move=True, no_collapse=True, no_close=True, no_resize=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass

			with dpg.window(
				label="Output", id="window_output", no_move=True, no_collapse=True, no_close=True, no_resize=True,
				min_size=(VIEWPORT_WIDTH/3, VIEWPORT_HEIGHT)):
				pass

		dpg.setup_viewport()
		dpg.set_viewport_title(title="Sm Injector Interface")
		dpg.set_viewport_width(VIEWPORT_WIDTH)
		dpg.set_viewport_height(VIEWPORT_HEIGHT)
		dpg.set_viewport_min_width(VIEWPORT_MIN_WIDTH)
		dpg.set_viewport_min_height(VIEWPORT_MIN_HEIGHT)
		dpg.set_viewport_vsync(True)

		dpg.set_viewport_resizable(True)

		def resize_viewport(_, size):
			viewport_width = dpg.get_viewport_width()
			viewport_height = dpg.get_viewport_height()

			for i, window in enumerate(("window_input", "window_module", "window_output")):
				dpg.set_item_pos(item=window, pos=((viewport_width/3) * i, 20))
				dpg.set_item_width(item=window, width=viewport_width/3)
				dpg.set_item_height(item=window, height=viewport_height)
		dpg.set_viewport_resize_callback(resize_viewport)

		dpg.set_primary_window("main_window", True)

		self.create_inputs_ui(input_controller)
		self.create_modules_ui(module_controller)
		self.create_outputs_ui(output_controller)

		resize_viewport(0, (0, 0))

	def create_inputs_ui(self, input_controller):
		for inp in input_controller.get_inputs():
			with dpg.group(parent="window_input", horizontal=True):
				dpg.add_button(label=str(inp))
				# with dpg.tooltip(parent=dpg.last_item()):
				# 	dpg.add_text("LOT OF DATA HERE")
				with dpg.drag_payload(parent=dpg.last_item(), drag_data=inp, payload_type="data"):
					dpg.add_text(str(inp))
				dpg.add_checkbox(label="", user_data=inp, callback=lambda id, value, udata : udata.switch(), default_value=False)

	def create_modules_ui(self, module_controller):
		for module in module_controller.get_modules():

			with dpg.child(parent="window_module", height=200, border=True):
				# IN
				dpg.add_text("IN", bullet=True)
				for key, inp in module._inputs.items():
					with dpg.group(horizontal=True):

						def callback(id, data):
							input_key, mod = dpg.get_item_user_data(id)

							if input_key in mod._inputs:
								mod._inputs[input_key] = data
							dpg.set_item_label(id, str(data))

						dpg.add_text(key)
						dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
							user_data=(key, module), drop_callback=callback)

				# OUT
				dpg.add_text("OUT", bullet=True)
				for key, out in module._outputs.items():
					with dpg.group(horizontal=True):

						dpg.add_button(label=key)
						with dpg.drag_payload(parent=dpg.last_item(), drag_data=(key, out), payload_type="data"):
							dpg.add_text(key)

						dpg.add_text("0.0")
						dpg.add_visible_handler(parent=id,
							user_data=(dpg.last_item(), key, module),
							callback=lambda id, _, data: dpg.set_value(data[0], data[2]._outputs[data[1]].get_value() ))

	def create_outputs_ui(self, output_controller):
		#TODO: replace this by a button to add them dynamically
		for i in range(4):
			output = Output()
			output_controller.outputs.append(output)

		for output in output_controller.outputs:
			with dpg.group(parent="window_output", horizontal=True):

				def callback(id, data):
					out = dpg.get_item_user_data(id)
					key, module_output = data

					dpg.set_item_label(id, key)
					out._input = module_output

				dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data",
					user_data=output,
					drop_callback=callback)

				def callback2(id, _, user_data):
					id_but, out = user_data
					if out:
						dpg.set_value(id_but, out.get_value())

				dpg.add_text("0.0")
				dpg.add_visible_handler(parent=dpg.last_item(),
					user_data=(dpg.last_item(), output),
					callback=callback2)

				dpg.add_input_int(default_value=0, width=100, min_value=0, max_value=255, step=1)

	def is_running(self):
		return dpg.is_dearpygui_running()

	def update(self):
		dpg.render_dearpygui_frame()

	def cleanup(self):
		dpg.cleanup_dearpygui()
