import time


class ArduinoInterface:
    def __init__(self):
        pass

    def convert_command_to_degrees_turn(self, next_movement):
        if next_movement == "Right":
            return 90
        if next_movement == "Left":
            return -90
        if next_movement == "Backwards" or next_movement == "Forward":
            return 0

    def goto(self, orientation, next_movement, going_to_color, scan=False):
        degress_to_turn = self.convert_command_to_degrees_turn(next_movement)
        print(f"{degress_to_turn} degress turn needed")
        time.sleep(2)
