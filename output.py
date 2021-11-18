class Output:
    def __init__(self):
        self._input = None #Var
        self._input_key = ""
        self._id = 0
        self._is_on = False

    def switch(self):
        self._is_on = not self._is_on

    def get_value(self):
        if self._input:
            return self._input.get_value()
        return 0.0

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

class OutputController:
    def __init__(self):
        self.outputs = [] #[Output]

    def add_output(self):
        output = Output()
        self.outputs.append(output)
        return output

    def send_outputs(self, injectionAPI):
        for output in self.outputs:
            if not output._is_on: continue
            if output._input:
                value = output._input.get_value()
                if value != None:
                    injectionAPI.set_value(output.get_id(), value)
