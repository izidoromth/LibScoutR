import time


class ArduinoInterface:
    def __init__(self):
        self.__done = True

    def done(self):
        self.__done = True

    def goto(self, came_from_color, current_color, next_color, scan=False):
        self.__done = False
        while self.__done == False:
            time.sleep(2)
            self.done()