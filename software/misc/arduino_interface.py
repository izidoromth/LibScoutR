import time
import serial

class ArduinoInterface:
    def __init__(self):
        self.arduino_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=30)
        self.arduino_serial.reset_output_buffer()
        self.arduino_serial.write('init'.encode('utf-8'))

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
            commands = commands + 'n'
        elif (scan == True):
            commands = commands + 'y'
        # region fix_camera
        if (fix_camera == False):
            commands = commands + '0'
        elif (fix_camera == True):
            commands = commands + '0'
        # endregion
        return commands

    def goto(
        self, orientation, next_movement, going_to_color, scan=False, fix_camera=False
    ):
        self.arduino_serial.reset_input_buffer()
        degrees_to_turn = self.convert_command_to_degrees_turn(next_movement)
        if fix_camera:
            degrees_to_turn = degrees_to_turn + 180
            if degrees_to_turn > 180:
                degrees_to_turn = degrees_to_turn - 360
        print(f"A {degrees_to_turn} degrees turn is needed")

        books_scanned_bottom = ['123 x23 iqw', '456 y12 8kk', '801 sin cos']
        books_scanned_top = ['123 x23 iqw', '456 y12 8kk', '801 sin cos']

        self.arduino_serial.reset_input_buffer()
        commands = self.map_to_bytes(orientation, next_movement, going_to_color, degrees_to_turn, scan, fix_camera)

        # while True:
        #     command = input('command')         
        #     self.arduino_serial.write(command.encode('utf-8'))
        #     self.arduino_serial.flush()

        #     response = self.arduino_serial.read_until(b'_eol')
        #     self.arduino_serial.reset_input_buffer()

        #     print(response.decode('utf-8'))
        
        time.sleep(1)

        # always flush after writing
        self.arduino_serial.write(commands.encode('utf-8'))
        self.arduino_serial.flush()
        
        while True:
            # for awaiting for arduino response use the folowing
            response = self.arduino_serial.read_until(b'_eol')
            self.arduino_serial.reset_input_buffer()

            # the response as a string needs to be decoded
            decoded_response = response.decode('utf-8')
            print(decoded_response)
            if decoded_response == 'okay_eol':
                print("qr detecting")
                # always flush after writing
                self.arduino_serial.write('next__'.encode('utf-8'))
                self.arduino_serial.flush()
                time.sleep(3)
            elif decoded_response == 'final_eol':
                break
            else:
                print('deu ruim')


            time.sleep(1)
        return True
