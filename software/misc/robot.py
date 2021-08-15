from library import Library
from arduino_interface import ArduinoInterface
import time
import random


class Robot:
    def __init__(self):
        self.__ascii_art = """
         _     _ _     _____                 _  ______
        | |   (_) |   /  ___|               | | | ___ \\
        | |    _| |__ \ `--.  ___ ___  _   _| |_| |_/ /
        | |   | | '_ \ `--. \/ __/ _ \| | | | __|    /
        | |___| | |_) /\__/ / (_| (_) | |_| | |_| |\ \\
        \_____/_|_.__/\____/ \___\___/ \__,_|\__\_| \_|

        """
        print(self.__ascii_art)
        # Library
        self.__library = Library()
        self.__library.setup()
        # Position knowledge
        self.__came_from_color = "Purple"
        self.__current_color = "Brown"
        self.__going_to_color = None
        self.__orientation = "Forward"
        self.__next_direction = None
        # Bool scan
        self.__scanning = None
        # Books to search
        self.__books_to_search = []
        # Scout path (can change internally)
        self.__scout_path = self.__library.get_scout_path()
        # Arduino interface
        self.__arduino = ArduinoInterface()

    def __LIS(self, book_list):
        # https://stackoverflow.com/questions/27324717/obtaining-the-longest-increasing-subsequence-in-python

        # make a list of lists
        sequences = list()
        for i in range(0, len(book_list)):
            sequences.append(list())

        for i in range(0, len(book_list)):
            for j in range(0, i):

                # a new larger increasing subsequence found
                if (
                    book_list[j].get_internal_code() < book_list[i].get_internal_code()
                ) and (len(sequences[i]) < len(sequences[j])):
                    # 'throw the previous list'
                    sequences[i] = []
                    # 'add all elements of sequences[j] to sequences[i]'
                    sequences[i].extend(sequences[j])
            sequences[i].append(book_list[i])

        max_length = max(len(seq) for seq in sequences)
        return [seq for seq in sequences if len(seq) == max_length]

    def __get_next_color_path(self, path, color):
        return path[(path.index(color) + 1) % len(path)]

    def __get_index(self, matrix, value):
        return next(
            (row.index(value), index)
            for index, row in enumerate(matrix)
            if value in row
        )

    def __get_relative_direction(self, start_color, end_color):
        movement = None

        start_x, start_y = start_color
        end_x, end_y = end_color

        if (start_x - end_x) == 1:
            movement = "Left"
        # Going Right
        elif (start_x - end_x) == -1:
            movement = "Right"
        # Going Up
        if (start_y - end_y) == 1:
            movement = "Up"
        # Going Down
        elif (start_y - end_y) == -1:
            movement = "Down"

        return movement

    def __get_next_direction(self, came_from_color, current_color, going_to_color):
        if going_to_color == None:
            return

        positions = self.__library.get_path_positions()

        came_from_index = self.__get_index(positions, came_from_color)
        current_index = self.__get_index(positions, current_color)
        going_to_index = self.__get_index(positions, going_to_color)

        last_movement_direction = self.__get_relative_direction(
            came_from_index, current_index
        )
        going_to_position = self.__get_relative_direction(current_index, going_to_index)
        output_direction = None

        if last_movement_direction == "Left":
            if going_to_position == "Right":
                if self.__orientation == "Forward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Forward"
                    self.__orientation = output_direction
            elif going_to_position == "Left":
                output_direction = self.__orientation
            elif going_to_position == "Up":
                output_direction = "Right"
            elif going_to_position == "Down":
                output_direction = "Left"

        elif last_movement_direction == "Right":
            if going_to_position == "Right":
                output_direction = self.__orientation
            elif going_to_position == "Left":
                if self.__orientation == "Forward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Forward"
                    self.__orientation = output_direction
            elif going_to_position == "Up":
                output_direction = "Left"
            elif going_to_position == "Down":
                output_direction = "Right"

        elif last_movement_direction == "Up":
            if going_to_position == "Right":
                output_direction = "Right"
            elif going_to_position == "Left":
                output_direction = "Left"
            elif going_to_position == "Up":
                output_direction = self.__orientation
            elif going_to_position == "Down":
                if self.__orientation == "Forward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Forward"
                    self.__orientation = output_direction

        elif last_movement_direction == "Down":
            if going_to_position == "Right":
                output_direction = "Left"
            elif going_to_position == "Left":
                output_direction = "Right"
            elif going_to_position == "Up":
                if self.__orientation == "Forward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Forward"
                    self.__orientation = output_direction
            elif going_to_position == "Down":
                output_direction = self.__orientation

        return output_direction

    def __check_if_camera_in_right_direction(
        self, current_color, going_to_color, orientation
    ):
        original_scout_path = self.__library.get_scout_path()
        reversed_scout_path = self.__library.get_scout_path()

        reversed_scout_path.reverse()
        # print("original path", original_scout_path)
        # print("reversed path", reversed_scout_path)
        next_color_forward = self.__get_next_color_path(
            original_scout_path, current_color
        )
        next_color_backwards = self.__get_next_color_path(
            reversed_scout_path, current_color
        )
        # print(f"checando {current_color}, {going_to_color}, {orientation}")
        # print(f"next color forward {next_color_forward}, next color backwards {next_color_backwards}")
        if next_color_forward == going_to_color and orientation == "Forward":
            return True
        elif next_color_backwards == going_to_color and orientation == "Backwards":
            return True
        else:
            # print("orientation false")
            return False

    def user_want_book(self, book_json):
        book_to_search = self.__library.generate_book_from_json(book_json)
        self.__books_to_search.append(book_to_search)
        return book_to_search.get_name()

    def print_position(self):
        print(self.__ascii_art)
        print(
            """
                1st row:                                    2nd row:
            ------Adventure----------Comic Books-----       ------Romance----------Science Fiction---
            |                   |                   |       |                   |                   |
            |                   |                   |       |                   |                   |
            |                   |                   |       |                   |                   |
            ------Detective-------------Horror-------       ------Suspense------------Biography------
            """
        )

        print(
            f"""
            {"🤖" if self.__current_color == "Orange" else "-"}---------{"⬅️" if (self.__going_to_color == "Orange"  and self.__current_color == "Red") else ("➡️" if (self.__going_to_color == "Red"  and self.__current_color == "Orange") else "-")}---------{"🤖" if self.__current_color == "Red" else "-"}---------{"⬅️" if (self.__going_to_color == "Red"  and self.__current_color == "Blue") else ("➡️" if (self.__going_to_color == "Blue"  and self.__current_color == "Red") else "-")}---------{"🤖" if self.__current_color == "Blue" else "-"}
            |                   |                   |
            {"⬇️" if (self.__going_to_color == "Brown"  and self.__current_color == "Orange") else ("⬆️" if (self.__going_to_color == "Orange"  and self.__current_color == "Brown") else "|")}                   {"⬇️" if (self.__going_to_color == "Purple"  and self.__current_color == "Red") else ("⬆️" if (self.__going_to_color == "Red"  and self.__current_color == "Purple") else "|")}                   {"⬇️" if (self.__going_to_color == "Yellow"  and self.__current_color == "Blue") else ("⬆️" if (self.__going_to_color == "Blue"  and self.__current_color == "Yellow") else "|")}
            |                   |                   |
            {"🤖" if self.__current_color == "Brown" else "-"}---------{"⬅️" if (self.__going_to_color == "Brown"  and self.__current_color == "Purple") else ("➡️" if (self.__going_to_color == "Purple"  and self.__current_color == "Brown") else "-")}---------{"🤖" if self.__current_color == "Purple" else "-"}---------{"⬅️" if (self.__going_to_color == "Purple"  and self.__current_color == "Yellow") else ("➡️" if (self.__going_to_color == "Yellow"  and self.__current_color == "Purple") else "-")}---------{"🤖" if self.__current_color == "Yellow" else "-"}
            """
        )

        if len(self.__books_to_search):
            book_to_search = self.__books_to_search[0]
            print(
                "Guiding user to book {0} in {1}".format(
                    book_to_search.get_name(), book_to_search.get_category()
                )
            )
        else:
            print("Scouting.")

        if self.__going_to_color:
            print(f"Direction: {self.__orientation}")
            print(f"Scanning = {self.__scanning}")
        else:
            print("\n\n")

    def organize_shelve(self, category, list_of_book_read):
        codes_read = list_of_book_read
        books_read = self.__library.create_book_list_from_code_list(codes_read)
        same_category_books = self.__library.filter_book_list_by_category(
            books_read, category
        )
        wrong_shelf_books = [
            book.get_universal_code() for book in books_read if book not in same_category_books
        ]
        correct_books = self.__LIS(same_category_books)
        incorrect_books = []
        for book in same_category_books:
            if book not in correct_books[0]:
                incorrect_books.append(book.get_universal_code())

        print("Oraganization plan:")
        return {"Wrong Shelve": wrong_shelf_books, "Out of Order": incorrect_books}

    def scout(self):
        self.__going_to_color = self.__get_next_color_path(
            self.__scout_path, self.__current_color
        )
        if self.__going_to_color == self.__came_from_color:
            self.__scout_path.reverse()
            self.__going_to_color = self.__get_next_color_path(
                self.__scout_path, self.__current_color
            )

        self.__next_direction = self.__get_next_direction(
            self.__came_from_color, self.__current_color, self.__going_to_color
        )

        if self.__library.edge_has_books([self.__current_color, self.__going_to_color]):
            self.__scanning = True
        else:
            self.__scanning = False

        camera_is_right = self.__check_if_camera_in_right_direction(
            self.__current_color, self.__going_to_color, self.__orientation
        )
        if camera_is_right == False:
            if self.__orientation == "Forward":
                self.__orientation = "Backwards"
            else:
                self.__orientation = "Forward"

        self.print_position()
        codes_scanned = self.__arduino.goto(
            self.__orientation,
            self.__next_direction,
            self.__going_to_color,
            scan=self.__scanning,
            fix_camera=(self.__scanning and not camera_is_right),
        )
        
        
        if self.__scanning:
            # {'1st floor': 'Adventure', '2nd floor': 'Romance'}
            scanning_these_categories = self.__library.get_categories_from_color_position(self.__current_color, self.__going_to_color,)
            
            # {'Wrong Shelve': ['7542.69', '7543.69'], 'Out of Order': ['2321.23']}
            # self.organize_shelve(scanning_these_categories['1st floor'], codes_scanned['1st floor'])
            
            # codes_scanned look like this:
            # {
            #   '1st floor': ['123 x23 iqw', '456 y12 8kk', '801 sin cos'],
            #   '2nd floor': ['123 x23 iqw', '456 y12 8kk', '801 sin cos']
            # }
            for book_code in codes_scanned:
                pass

        self.__came_from_color = self.__current_color
        self.__current_color = self.__going_to_color
        self.__going_to_color = None
        self.print_position()

        time.sleep(2)

    def guide_user(self, desired_book):
        path = self.__library.find_path(
            self.__current_color, desired_book.get_category()
        )
        path_size = len(path)
        self.__going_to_color = path[0]
        self.__next_direction = self.__get_next_direction(
            self.__came_from_color, self.__current_color, self.__going_to_color
        )

        for i in range(path_size):
            if i != (path_size - 1):
                self.__scanning = False
                self.print_position()

                self.__arduino.goto(
                    self.__orientation,
                    self.__next_direction,
                    self.__going_to_color,
                    scan=self.__scanning,
                )
                self.__came_from_color = self.__current_color
                self.__current_color = self.__going_to_color
                path.pop(0)
                self.__going_to_color = path[0]
                self.__next_direction = self.__get_next_direction(
                    self.__came_from_color, self.__current_color, self.__going_to_color
                )

            else:
                self.__scanning = True
                camera_is_right = self.__check_if_camera_in_right_direction(
                    self.__current_color, self.__going_to_color, self.__orientation
                )
                if camera_is_right == False:
                    if self.__orientation == "Forward":
                        self.__orientation = "Backwards"
                    else:
                        self.__orientation = "Forward"
                self.print_position()
                self.__arduino.goto(
                    self.__orientation,
                    self.__next_direction,
                    self.__going_to_color,
                    scan=self.__scanning,
                    fix_camera=(self.__scanning and not camera_is_right),
                )
                self.__came_from_color = self.__current_color
                self.__current_color = self.__going_to_color
                self.__going_to_color = None
                self.print_position()
                time.sleep(2)

        self.__books_to_search.pop(0)
        print("Finish guiding user")

    def main(self):
        while True:
            if len(self.__books_to_search):
                self.guide_user(self.__books_to_search[0])
            else:
                self.scout()
