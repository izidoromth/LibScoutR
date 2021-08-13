import time
import serial

class ArduinoInterface:
    def __init__(self):
        self.arduino_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        self.arduino_serial.timeout = 30

    def convert_command_to_degrees_turn(self, next_movement):
        if next_movement == "Right":
            return 90
        if next_movement == "Left":
            return -90
        if next_movement == "Backwards" or next_movement == "Forward":
            return 0
    
    def map_to_bytes(self, orientation, next_movement, going_to_color, 
    degrees_to_turn, scan, fix_camera):

        commands = ''
        # region orientation
        if(orientation == "Forward"):
            commands = commands + 'f'
        elif(orientation == "Backwards"):
            commands = commands + 'b'
        # endregion
        # region next_movement
        if(next_movement == "Right"):
            commands = commands + '0'
        elif(next_movement == "Left"):
            commands = commands + '0'
        elif (next_movement == "Forward"):
            commands = commands + '0'
        elif (next_movement == "Backwards"):
            commands = commands + '0'
        # endregion
        # region going_to_color
        if (going_to_color == "Orange"):
            commands = commands + '0'
        elif (going_to_color == "Red"):
            commands = commands + '0'
        elif (going_to_color == "Blue"):
            commands = commands + '0'
        elif (going_to_color == "Brown"):
            commands = commands + '0'
        elif (going_to_color == "Purple"):
            commands = commands + '0'
        elif (going_to_color == "Yellow"):
            commands = commands + '0'
        # endregion
        # region degrees_to_turn
        if (degrees_to_turn == 0):
            commands = commands + 's'
        elif (degrees_to_turn == 90):
            commands = commands + 'p'
        elif (degrees_to_turn == -90):
            commands = commands + 'n'
        elif (degrees_to_turn == 180):
            commands = commands + 'c'
        # endregion
        # region scan
        if (scan == False):
            commands = commands + 'y'
        elif (scan == True):
            commands = commands + 'n'
        # region fix_camera
        if (fix_camera == False):
            commands = commands + '0'
        elif (fix_camera == True):
            commands = commands + '0'
        # endregion
        commands = commands + '\n'
        return commands

    def goto(
        self, orientation, next_movement, going_to_color, scan=False, fix_camera=False
    ):
        self.arduino_serial.reset_input_buffer()
        color_read = None
        degrees_to_turn = self.convert_command_to_degrees_turn(next_movement)
        if fix_camera:
            degrees_to_turn = degrees_to_turn + 180
            if degrees_to_turn > 180:
                degrees_to_turn = degrees_to_turn - 360
        print(f"A {degrees_to_turn} degrees turn is needed")
        
        commands = self.map_to_bytes(orientation, next_movement, going_to_color, degrees_to_turn, scan, fix_camera)

        # always flush after writing
        self.arduino_serial.write(commands.encode('utf-8'))
        self.arduino_serial.flush()
        
        # for awaiting for arduino response use the folowing
        response = self.arduino_serial.read_until(b'final')
        self.arduino_serial.reset_input_buffer()

        # the response as a string needs to be decoded
        print(response.decode('utf-8'))
        time.sleep(1)
        return color_read
