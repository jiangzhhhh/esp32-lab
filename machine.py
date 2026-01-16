class Pin:
    OUT = 0
    IN = 1

    def __init__(self, pin_number, mode):
        self.pin_number = pin_number
        self.mode = mode

    def value(self, value):
        pass

    def on(self):
        pass

    def off(self):
        pass