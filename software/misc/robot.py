from library import Library
from arduino_interface import ArduinoInterface
from book import Book
import threading
import time
import random
import os


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
        self.__current_category = None
        self.__going_to_color = None
        self.__books_to_search = []
        self.__scout_path = ["Orange", "Red", "Blue", "Yellow", "Purple", "Brown"]
        self.__library = Library()
        self.__library.setup()
        self.__arduino = ArduinoInterface()
        threading.Thread(target=self.__wait_for_user).start()

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

    def __wait_for_user(self):
        while True:
            random_time = random.randrange(20, 40)
            time.sleep(random_time)

            books = self.__library.get_books()
            book_to_search = books[random.randrange(len(books))]
            print(
                "\n\n---------------\nRequest to search for {0} in category {1}\n---------------\n".format(
                    book_to_search.get_name(), book_to_search.get_category()
                )
            )
            self.__books_to_search.append(book_to_search)

    def print_position(self):
        os.system("cls||clear")
        print(self.__ascii_art)
        print(
            """
            ORANGE-------------RED---------------BLUE
            |                   |                   |
            |                   |                   |
            |                   |                   |
            BROWN------------PURPLE------------YELLOW
            """
        )
        if len(self.__books_to_search):
            print(
                "Guiding user to book {0}".format(self.__books_to_search[0].get_name())
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
        self.print_position()
        # print(
        #     "In color: {0}. Came from {1}. Going to {2}".format(
        #         self.__current_color, self.__came_from_color, next_color
        #     )
        # )
        if self.__library.edge_has_books([self.__current_color, self.__going_to_color]):
            self.__arduino.goto(
                self.__came_from_color,
                self.__current_color,
                self.__going_to_color,
                scan=True,
            )
        else:
            self.__arduino.goto(
                self.__came_from_color,
                self.__current_color,
                self.__going_to_color,
                scan=False,
            )
        self.__came_from_color = self.__current_color
        self.__current_color = self.__going_to_color

    def guide_user(self, desired_book):
        # print("Guiding user to book {0}".format(desired_book.get_name()))
        path = self.__library.find_path(
            self.__current_color, desired_book.get_category()
        )
        path_size = len(path)
        print(
            "Path to {1} from {0} is".format(
                self.__current_color, desired_book.get_category()
            ),
            *path,
        )
        print()
        self.__going_to_color = path[0]
        self.print_position()
        # print(
        #     "In color: {0}. Came from {1}. Going to {2}".format(
        #         self.__current_color, self.__came_from_color, next_color
        #     )
        # )

        for i in range(path_size):
            if i != (path_size - 1):
                self.__arduino.goto(
                    self.__came_from_color, self.__current_color, path[0], scan=False
                )
                self.__came_from_color = self.__current_color
                self.__current_color = self.__going_to_color
                path.pop(0)
                self.__going_to_color = path[0]
                self.print_position()
                # print(
                #     "In color: {0}. Came from {1}. Going to {2}".format(
                #         self.__current_color, self.__came_from_color, next_color
                #     )
                # )
            else:
                self.__arduino.goto(
                    self.__came_from_color, self.__current_color, path[0], scan=True
                )
                self.__came_from_color = self.__current_color
                self.__current_color = self.__going_to_color
                self.print_position()
                # print(
                #     "In color: {0}. Came from {1}".format(
                #         self.__current_color, self.__came_from_color
                #     )
                # )

        self.__books_to_search.pop(0)
        print("Finish guiding user")

    def main(self):
        while True:
            if len(self.__books_to_search):
                self.guide_user(self.__books_to_search[0])
            else:
                self.scout()


robot = Robot()
# alan_turing = Book("Alan Turing", "2321.23", "Biography")
# robot.guide_user(alan_turing)
robot.main()
