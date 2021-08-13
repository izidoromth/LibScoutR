import time
import serial

class ArduinoInterface:
    def __init__(self):
        self.arduino_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

    def convert_command_to_degrees_turn(self, next_movement):
        if next_movement == "Right":
            return 90
        if next_movement == "Left":
            return -90
        if next_movement == "Backwards" or next_movement == "Forward":
            return 0
    
    def map_to_bytes(self, orientation, next_movement, going_to_color, 
    degrees_to_turn, scan, fix_camera):

        commands = []
        # region orientation
        if(orientation == "Forward"):
            commands.append('f')
        elif(orientation == "Backwards"):
            commands.append('b')
        # endregion
        # region next_movement
        if(next_movement == "Right"):
            commands.append('')
        elif(next_movement == "Left"):
            commands.append('')
        elif (next_movement == "Forward"):
            commands.append('')
        elif (next_movement == "Backwards"):
            commands.append('')
        # endregion
        # region going_to_color
        if (going_to_color == "Orange"):
            commands.append('')
        elif (going_to_color == "Red"):
            commands.append('')
        elif (going_to_color == "Blue"):
            commands.append('')
        elif (going_to_color == "Brown"):
            commands.append('')
        elif (going_to_color == "Purple"):
            commands.append('')
        elif (going_to_color == "Yellow"):
            commands.append('')
        # endregion
        # region degrees_to_turn
        if (degrees_to_turn == 0):
            commands.append('s')
        elif (degrees_to_turn == 90):
            commands.append('p')
        elif (degrees_to_turn == -90):
            commands.append('n')
        elif (degrees_to_turn == 180):
            commands.append('c')
        # endregion
        # region scan
        if (scan == False):
            commands.append('')
        elif (scan == True):
            commands.append('')
        # region fix_camera
        if (fix_camera == False):
            commands.append('')
        elif (fix_camera == True):
            commands.append('')
        # endregion
        if(len(commands) != 6):
            print("Erro ao fazer mapeamento")

        return commands

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
        
        commands = self.map_to_bytes(orientation, next_movement, going_to_color, degrees_to_turn, scan, fix_camera)
        
        for i in range(len(commands)):
            self.arduino_serial.write(commands[i].encode('utf-8'))
            time.sleep(0.1)
        
        print(commands)
        while True:
            response = None
            while self.arduino_serial.in_waiting:
                pass

            response = self.arduino_serial.readline()
            self.arduino_serial.flush()
            time.sleep(0.1)

            print(response)
            if response == 'ok':
                print("qr detecting")
                self.arduino_serial.write("next".encode('utf-8'))
                time.sleep(0.1)
            elif response == 'final':
                break
            else:
                print("deu ruim")

            time.sleep(0.5)

        return color_read
