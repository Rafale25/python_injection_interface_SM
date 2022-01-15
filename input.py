import pygame
# import math #DEBUG

from var import Var

# class VarMisc(Var):
#     def __init__():
#         self.

#gamepad
class Input(Var):
    def __init__(self, joystick, id, input_type):
        self._joystick = joystick
        self._id = id
        self._input_type = input_type

        self._is_on = False
        self._invert = False

        # self.tmp = 0.0 #DEBUG
        self.set_name(str(self))

    def __str__(self):
        return "{} {}".format(self._input_type, self._id)

    def __repr__(self):
        return "{};{};{};{}".format(self._id, self._input_type, self._var, self._is_on)

    def is_on(self):
        return self._is_on

    # def get_var(self):
    #     return self._var

    # def get_value(self):
    #     return self._var.get_value()

    def invert(self):
        self._invert = not self._invert

    def switch(self):
        self._is_on = not self._is_on

    def update(self):
        new_value = 0

        if self._input_type == 'numball':
            new_value = self._joystick.get_ball(self._id)
        elif self._input_type == 'axis':
            new_value = self._joystick.get_axis(self._id)
        elif self._input_type == 'button':
            new_value = self._joystick.get_button(self._id)
        elif self._input_type == 'hat':
            new_value = self._joystick.get_hat(self._id)

        # self.tmp += 0.01
        # new_value = (math.sin(self.tmp) + 1)/2

        if self._invert:
            new_value = -new_value
        self.set_value(new_value)

class InputController:
    def __init__(self):
        ## gamepads
        self.inputs = []
        self.joysticks = []

        ## SM_output
        self.inputs_SMoutput = {} #{id, SMoutput, SMid}

        ## Misc
        self.inputs_misc = {} #{id, input_misc}

    def scan_joysticks(self):
        joystick_count = pygame.joystick.get_count()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(joystick_count)]

    def add_SMoutput(self):
        # find smallest unused id
        l = [id for id in self.inputs_SMoutput]
        id = next(i for i, e in enumerate(sorted(l) + [ None ], 1) if i != e)

        e = Var()
        e.set_name(f"SMoutput {id}")
        self.inputs_SMoutput[id] = [e, 0]
        return id, e

    # add misc input to list
    def add_misc(self):
        # find smallest unused id
        l = [id for id in self.inputs_misc]
        id = next(i for i, e in enumerate(sorted(l) + [ None ], 1) if i != e)

        misc = Var()
        misc.set_name(misc.get_name() + f" {id}")
        self.inputs_misc[id] = misc
        return id, misc

    def init_inputs(self):
        for joystick in self.joysticks:
            for i in range(joystick.get_numballs()):
                inp = Input(joystick=joystick, id=i, input_type="numball")
                self.inputs.append(inp)
            for i in range(joystick.get_numaxes()):
                inp = Input(joystick=joystick, id=i, input_type="axis")
                self.inputs.append(inp)
            for i in range(joystick.get_numbuttons()):
                inp = Input(joystick=joystick, id=i, input_type="button")
                self.inputs.append(inp)
            for i in range(joystick.get_numhats()):
                inp = Input(joystick=joystick, id=i, input_type="hat")
                self.inputs.append(inp)

    def get_inputs(self):
        return self.inputs

    def update(self, injectionAPI):
        # get ids to ask value from game
        ids = [SMid for id, (var, SMid) in self.inputs_SMoutput.items()]
        if ids:
            injectionAPI.ask_value(ids)
            data = injectionAPI.recv_value()

            for SMid1, value in data:
                for id, (var, SMid2) in self.inputs_SMoutput.items():
                    if SMid1 == SMid2:
                        var.set_value(value)

        for inp in self.inputs:
            if inp.is_on():
                inp.update()
            else:
                inp.set_value(0.0)
