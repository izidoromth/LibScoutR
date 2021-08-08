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

    def goto(
        self, orientation, next_movement, going_to_color, scan=False, fix_camera=False
    ):
        color_read = None
        degress_to_turn = self.convert_command_to_degrees_turn(next_movement)
        if fix_camera:
            degress_to_turn = degress_to_turn + 180
            if degress_to_turn > 180:
                degress_to_turn = degress_to_turn - 360
        print(f"A {degress_to_turn} degrees turn is needed")
        time.sleep(2)
        return color_read
