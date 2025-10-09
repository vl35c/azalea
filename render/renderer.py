class HeldFunction:
    def __init__(self, func, z: int):
        self.func = func
        self.z = z

    def call(self):
        self.func()


# renderer allows graphics to be rendered in any order regardless of where they were originally called
class Renderer:
    def __init__(self):
        self.held_functions: list[HeldFunction] = []

    # add function to list
    def hold(self, func, z: int):
        self.held_functions.append(HeldFunction(func, z))

    # sort functions by z layer and then call all
    def call(self):
        for function in sorted(self.held_functions, key=lambda f: f.z):
            function.call()
        self.flush()

    # clear function call list
    def flush(self):
        self.held_functions = []
