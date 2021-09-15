import os
import importlib

from var import Var

# MODULES --
class Module:
	def __init__(self):
		self._name = ""
		self._inputs = dict() #{key: Input}
		self._outputs = dict() #{key: Float}

	def set_name(self, str):
		self._name = str

	def get_name(self):
		return self._name

	# def get_outputs_keys(self):
	# 	return [key for key, value in self._outputs.items()]

	# def get_inputs_dict(self):
	# 	return self._inputs

	# def get_outputs_dict(self):
	# 	return self._outputs

	def add_input(self, key):
		self._inputs[key] = None

	def add_output(self, key):
		self._outputs[key] = Var(0.0)

	def get_input(self, key):
		if self._inputs[key] != None:
			return self._inputs[key].get_value()
		return 0.0

	def set_output(self, key, value):
		self._outputs[key].set_value(value)

	def compute(self):
		pass

class ModuleController:
	MODULE_FOLDER_PATH = "./modules"

	def __init__(self):
		self.modules_classes = []
		self.module_instances = []

	def get_modules(self):
		return self.module_instances

	def get_outputs_items(self):
		items = {}
		for module in self.module_instances:
			items.update(module.get_outputs())
		return items

	def get_outputs_keys(self):
		keys = []
		for module in self.module_instances:
			keys.extend(module.get_outputs_keys())
		return keys

	def create_modules_dynamically(self):
		# import class dynamically and instantiate them
		modules_names = [path.split('.')[0] for path in os.listdir(ModuleController.MODULE_FOLDER_PATH) if path[-2:] == "py"]
		for name in modules_names:
			module = importlib.import_module("modules.{}".format(name))
			ModuleClass = getattr(module, name)
			self.modules_classes.append(ModuleClass)

		# TODO: Change later
		# create an instance of every class/module
		for ModuleCLass in self.modules_classes:
			self.module_instances.append( ModuleCLass() )

	def compute(self):
		for module in self.module_instances:
			module.compute()
