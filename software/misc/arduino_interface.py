import time
import serial
from qr_detection_standalone import qr_detect


class ArduinoInterface:
    def __init__(self):
        self.arduino_serial = serial.Serial(
            port="/dev/ttyACM0", baudrate=9600, timeout=30
        )
        self.arduino_serial.reset_output_buffer()
        self.arduino_serial.write("init".encode("utf-8"))

    def generate_list_from_parts(self, list_with_lists, orientation):
        my_set = set()
        final_list = []
        if orientation == "Backwards":
            list_with_lists.reverse()
        for list in list_with_lists:
            for code in list:
                if code not in my_set:
                    my_set.add(code)
                    final_list.append(code)

        return final_list

    def convert_command_to_degrees_turn(self, next_movement):
        if next_movement == "Right":
            return 90
        if next_movement == "Left":
            return -90
        if next_movement == "Backwards" or next_movement == "Forward":
            return 0

    def map_to_bytes(
        self,
        orientation,
        next_movement,
        going_to_color,
        degrees_to_turn,
        scan,
        fix_camera,
    ):

        commands = ""
        # region orientation
        if orientation == "Forward":
            commands = commands + "f"
        elif orientation == "Backwards":
            commands = commands + "b"
        # endregion
        # region next_movement
        if next_movement == "Right":
            commands = commands + "0"
        elif next_movement == "Left":
            commands = commands + "0"
        elif next_movement == "Forward":
            commands = commands + "0"
        elif next_movement == "Backwards":
            commands = commands + "0"
        # endregion
        # region going_to_color
        if going_to_color == "Orange":
            commands = commands + "0"
        elif going_to_color == "Red":
            commands = commands + "0"
        elif going_to_color == "Blue":
            commands = commands + "0"
        elif going_to_color == "Brown":
            commands = commands + "0"
        elif going_to_color == "Purple":
            commands = commands + "0"
        elif going_to_color == "Yellow":
            commands = commands + "0"
        # endregion
        # region degrees_to_turn
        if degrees_to_turn == 0:
            commands = commands + "s"
        elif degrees_to_turn == 90:
            commands = commands + "p"
        elif degrees_to_turn == -90:
            commands = commands + "n"
        elif degrees_to_turn == 180:
            commands = commands + "c"
        # endregion
        # region scan
        if scan == False:
            commands = commands + "n"
        elif scan == True:
            commands = commands + "y"
        # region fix_camera
        if fix_camera == False:
            commands = commands + "0"
        elif fix_camera == True:
            commands = commands + "0"
        # endregion
        return commands

    def goto(
        self, orientation, next_movement, going_to_color, scan=False, fix_camera=False
    ):
        degrees_to_turn = self.convert_command_to_degrees_turn(next_movement)
        if fix_camera:
            degrees_to_turn = degrees_to_turn + 180
            if degrees_to_turn > 180:
                degrees_to_turn = degrees_to_turn - 360
        print(f"A {degrees_to_turn} degrees turn is needed")

        commands = self.map_to_bytes(
            orientation,
            next_movement,
            going_to_color,
            degrees_to_turn,
            scan,
            fix_camera,
        )

        books_scanned_bottom = []
        books_scanned_top = []

        self.arduino_serial.reset_input_buffer()
        time.sleep(1)

        # always flush after writing
        self.arduino_serial.write(commands.encode("utf-8"))
        self.arduino_serial.flush()

        while True:
            # for awaiting for arduino response use the folowing
            response = self.arduino_serial.read_until(b"_eol")
            self.arduino_serial.reset_input_buffer()

            # the response as a string needs to be decoded
            decoded_response = response.decode("utf-8")
            print(decoded_response)
            if decoded_response == "okay_eol":
                print("QR detecting")
                bottom_detection = qr_detect(
                    camera_address=0,
                    exposition_iterations=50,
                    crop_top=0,
                    crop_bottom=0,
                    horz_res=1920,
                    vert_res=1080,
                    display_capture=False,
                )
                print(bottom_detection)
                books_scanned_bottom.append(bottom_detection)
                # ------------------
                # top_detection = qr_detect(
                #     camera_address=1,
                #     exposition_iterations=50,
                #     crop_top=0,
                #     crop_bottom=0,
                #     horz_res=1920,
                #     vert_res=1080,
                #     display_capture=False,
                # )
                # print(top_detection)
                # books_scanned_top.append(top_detection)
                # # ------------------
                # always flush after writing
                self.arduino_serial.write("next__".encode("utf-8"))
                self.arduino_serial.flush()
                time.sleep(3)
            elif decoded_response == "final_eol":
                break
            else:
                print("deu ruim")
            time.sleep(1)

        final_list_bottom = self.generate_list_from_parts(
            books_scanned_bottom, orientation
        )
        print("Final result bottom row: ", final_list_bottom)
        # --------------
        final_list_top = self.generate_list_from_parts(books_scanned_top, orientation)
        print("Final result top row: ", final_list_top)

        return {"1st floor": final_list_bottom, "2nd floor": final_list_top}
