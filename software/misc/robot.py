from library import Library
from arduino_interface import ArduinoInterface
from book import Book
import threading
import time
import random
import os

USER_INPUT_SLEEP = 10


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
        self.__came_from_color = "Purple"
        self.__current_color = "Brown"
        # self.__current_category = None
        self.__going_to_color = None
        self.__scanning = None
        self.__books_to_search = []
        self.__scout_path = ["Orange", "Red", "Blue", "Yellow", "Purple", "Brown"]
        self.__library = Library()
        self.__library.setup()
        self.__arduino = ArduinoInterface()
        self.__orientation = "Foward"
        self.__next_direction = None

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
            (row.index(value), index) for index, row in enumerate(matrix) if value in row
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
            return "aa"

        dir = [
            ["Orange", "Red", "Blue"],
            ["Brown", "Purple", "Yellow"],
        ]

        came_from_index = self.__get_index(dir, came_from_color)
        current_index = self.__get_index(dir, current_color)
        going_to_index = self.__get_index(dir, going_to_color)

        last_movement_direction = self.__get_relative_direction(came_from_index, current_index)
        going_to_position = self.__get_relative_direction(current_index, going_to_index)
        output_direction = None

        if last_movement_direction == "Left":
            if going_to_position == "Right":
                if self.__orientation == "Foward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Foward" 
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
                if self.__orientation == "Foward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Foward" 
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
                if self.__orientation == "Foward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Foward" 
                    self.__orientation = output_direction

        elif last_movement_direction == "Down":
            if going_to_position == "Right":
                output_direction = "Left"
            elif going_to_position == "Left":
                output_direction = "Right"
            elif going_to_position == "Up":
                if self.__orientation == "Foward":
                    output_direction = "Backwards"
                    self.__orientation = output_direction
                else:
                    output_direction = "Foward" 
                    self.__orientation = output_direction
            elif going_to_position == "Down":
                output_direction = self.__orientation

        # if self.__orientation == "Backwards":
        #     if output_direction == "Left":
        #         output_direction = "Right"
        #     elif output_direction == "Right":
        #         output_direction = "Left"


        return output_direction

    def user_want_book(self):
        books = self.__library.get_books()
        book_to_search = books[random.randrange(len(books))]
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
            print(f'Direction: {self.__orientation}. Next Movement: {self.__next_direction}')
            print(f"Scanning = {self.__scanning}")
        else:
            print('\n')

    def read_shelve(self):
        list_of_codes_read = [
            "102.1x",  # Ed Sheeran
            "2321.23",  # Alan Turing
            "43442.aa2",  # Steve Jobs
            "7542.69",  # Lupin
            "7543.69",  # Scooby Doo
        ]
        return list_of_codes_read

    def organize_shelve(self, category):
        codes_read = self.read_shelve()
        books_read = self.__library.create_book_list_from_code_list(codes_read)
        same_category_books = self.__library.filter_book_list_by_category(
            books_read, category
        )
        wrong_shelf_books = [
            book for book in books_read if book not in same_category_books
        ]
        correct_books = self.__LIS(same_category_books)
        incorrect_books = []
        for book in same_category_books:
            if book not in correct_books[0]:
                incorrect_books.append(book)

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

        if self.__library.edge_has_books([self.__current_color, self.__going_to_color]):
            self.__scanning = True
        else:
            self.__scanning = False

        self.__next_direction = self.__get_next_direction(self.__came_from_color, self.__current_color, self.__going_to_color)

        self.print_position()
        self.__arduino.goto(
            self.__came_from_color,
            self.__current_color,
            self.__going_to_color,
            scan=self.__scanning,
        )
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
        self.__next_direction = self.__get_next_direction(self.__came_from_color, self.__current_color, self.__going_to_color)
        
        for i in range(path_size):
            if i != (path_size - 1):
                self.__scanning = False
                self.print_position()

                self.__arduino.goto(
                    self.__came_from_color,
                    self.__current_color,
                    path[0],
                    scan=self.__scanning,
                )
                self.__came_from_color = self.__current_color
                self.__current_color = self.__going_to_color
                path.pop(0)
                self.__going_to_color = path[0]
                self.__next_direction = self.__get_next_direction(self.__came_from_color, self.__current_color, self.__going_to_color)

            else:
                self.__scanning = True
                self.print_position()
                self.__arduino.goto(
                    self.__came_from_color,
                    self.__current_color,
                    path[0],
                    scan=self.__scanning,
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
