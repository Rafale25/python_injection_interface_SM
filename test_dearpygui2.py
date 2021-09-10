#! /usr/bin/python3

import dearpygui.dearpygui as dpg

# with dpg.group(horizontal=True):

with dpg.window(label="Tutorial"):

	dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data")
	with dpg.drag_payload(parent=dpg.last_item(), drag_data=["yolo", "salut"], payload_type="data"):
		dpg.add_text("input 1")

	def callback(id, inp, user_data):
		print(f"id is: {id}")
		print(f"inp is: {inp}")
		print(f"user_data is: {user_data}")

	dpg.add_text("input 1")
	dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data", drop_callback=callback, user_data="HEYY")
	dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data", drop_callback=lambda id, data: callback(id, data, "heyy"))


dpg.start_dearpygui()




for module in module_controller.get_modules():

	with dpg.child(parent="window_module", height=150, border=True):
		# IN
		dpg.add_text("IN", bullet=True)
		print(module._inputs)

		for key, inp in module._inputs.items():
			with dpg.group(horizontal=True):

				def callback(id, data, input_key):
					print(f"id is: {id}")
					print(f"data is: {data}")
					print(f"input_key is: {input_key}")


				dpg.add_text(key)
				print("key: ", key)
				dpg.add_button(label="", width=75, height=20, enabled=False, payload_type="data", drop_callback=lambda id, data: callback(id, data, key) )
