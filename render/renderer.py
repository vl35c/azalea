class HeldFunction:
    def __init__(self, func, z: int):
        self.func = func
        self.z = z

    def call(self):
        self.func()


class Renderer:
    def __init__(self):
        self.held_functions: list[HeldFunction] = []

    def hold(self, func, z: int):
        self.held_functions.append(HeldFunction(func, z))

    def call(self):
        for function in sorted(self.held_functions, key=lambda f: f.z):
            function.call()
        self.flush()

    def flush(self):
        self.held_functions = []
