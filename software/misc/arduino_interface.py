import time
import serial

class ArduinoInterface:
    def __init__(self):
        self.arduino_serial = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

    def convert_command_to_degrees_turn(self, next_movement):
        if next_movement == "Right":
            return 90
        if next_movement == "Left":
            return -90
        if next_movement == "Backwards" or next_movement == "Forward":
            return 0
    
    def map_to_bytes(self, orientation, next_movement, going_to_color, 
    degrees_to_turn, scan, fix_camera):

        byte_list = bytearray()
        # region orientation
        if(orientation == "Forward"):
            byte_list += bytes([0x1])
        elif(orientation == "Backwards"):
            byte_list += bytes([0x2])
        # endregion
        # region next_movement
        if(next_movement == "Right"):
            byte_list += bytes([0x1])
        elif(next_movement == "Left"):
            byte_list += bytes([0x2])
        elif (next_movement == "Forward"):
            byte_list += bytes([0x3])
        elif (next_movement == "Backwards"):
            byte_list += bytes([0x4])
        # endregion
        # region going_to_color
        if (going_to_color == "Orange"):
            byte_list += bytes([0x1])
        elif (going_to_color == "Red"):
            byte_list += bytes([0x2])
        elif (going_to_color == "Blue"):
            byte_list += bytes([0x3])
        elif (going_to_color == "Brown"):
            byte_list += bytes([0x4])
        elif (going_to_color == "Purple"):
            byte_list += bytes([0x5])
        elif (going_to_color == "Yellow"):
            byte_list += bytes([0x6])
        # endregion
        # region degrees_to_turn
        if (degrees_to_turn == 0):
            byte_list += bytes([0x1])
        elif (degrees_to_turn == 90):
            byte_list += bytes([0x2])
        elif (degrees_to_turn == -90):
            byte_list += bytes([0x3])
        elif (degrees_to_turn == 180):
            byte_list += bytes([0x4])
        # endregion
        # region scan
        if (scan == False):
            byte_list += bytes([0x1])
        elif (scan == True):
            byte_list += bytes([0x2])
        # region fix_camera
        if (fix_camera == False):
            byte_list += bytes([0x1])
        elif (fix_camera == True):
            byte_list += bytes([0x2])
        # endregion
        if(len(byte_list) != 6):
            print("Erro ao fazer mapeamento")

        return byte_list

    def goto(
        self, orientation, next_movement, going_to_color, scan=False, fix_camera=False
    ):
        color_read = None
        degrees_to_turn = self.convert_command_to_degrees_turn(next_movement)
        if fix_camera:
            degrees_to_turn = degrees_to_turn + 180
            if degrees_to_turn > 180:
                degrees_to_turn = degrees_to_turn - 360
        print(f"A {degrees_to_turn} degrees turn is needed")
        byte_list = self.map_to_bytes(orientation, next_movement, going_to_color, degrees_to_turn, scan, fix_camera)
        print(byte_list)
        self.arduino_serial.write(byte_list)
        data = None
        while self.arduino_serial.in_waiting:
            data = self.arduino_serial.readline()
        print(data)
        time.sleep(0.5)
        return color_read
