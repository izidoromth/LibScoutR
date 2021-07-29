from library import Library
from arduino_interface import ArduinoInterface
from book import Book


class Robot:
    def __init__(self):
        print(
            """
         _     _ _     _____                 _  ______
        | |   (_) |   /  ___|               | | | ___ \\
        | |    _| |__ \ `--.  ___ ___  _   _| |_| |_/ /
        | |   | | '_ \ `--. \/ __/ _ \| | | | __|    /
        | |___| | |_) /\__/ / (_| (_) | |_| | |_| |\ \\
        \_____/_|_.__/\____/ \___\___/ \__,_|\__\_| \_|

        """
        )
        self.__came_from_color = "Brown"
        self.__current_color = "Orange"
        self.__current_category = None
        self.__in_scout_mode = False
        self.__scout_path = ["Orange", "Red", "Blue", "Yellow", "Purple", "Brown"]
        self.__library = Library()
        self.__library.setup()
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

    def get_next_color_path(self, path, color):
        return path[(path.index(color) + 1) % len(path)]

    def scout(self):
        next_color = self.get_next_color_path(self.__scout_path, self.__current_color)
        if next_color == self.__came_from_color:
            self.__scout_path.reverse()
            next_color = self.get_next_color_path(self.__scout_path, self.__current_color)
           
        print(
            "In color: {0}. Came from {1}. Going to {2}".format(
                self.__current_color, self.__came_from_color, next_color
            )
        )
        if self.__library.edge_has_books([self.__current_color, next_color]):
            self.__arduino.goto(
                self.__came_from_color, self.__current_color, next_color, scan=True
            )
        else:
            self.__arduino.goto(
                self.__came_from_color, self.__current_color, next_color, scan=False
            )
        self.__came_from_color = self.__current_color
        self.__current_color = next_color

    def guide_user(self, desired_book):
        path = self.__library.find_path(
            self.__came_from_color, desired_book.get_category()
        )
        path_size = len(path)
        print(path)
        next_color = path[0]
        print(
            "In color: {0}. Came from {1}. Going to {2}".format(
                self.__current_color, self.__came_from_color, next_color
            )
        )

        for i in range(path_size):
            if i != (path_size - 1):
                self.__arduino.goto(
                    self.__came_from_color, self.__current_color, path[0], scan=False
                )
                self.__came_from_color = self.__current_color
                self.__current_color = next_color
                path.pop(0)
                next_color = path[0]
                print(
                    "In color: {0}. Came from {1}. Going to {2}".format(
                        self.__current_color, self.__came_from_color, next_color
                    )
                )
            else:
                self.__arduino.goto(
                    self.__came_from_color, self.__current_color, path[0], scan=True
                )
                self.__came_from_color = self.__current_color
                self.__current_color = next_color
                print(
                    "In color: {0}. Came from {1}".format(
                        self.__current_color, self.__came_from_color
                    )
                )

    def main(self):
        while True:
            if self.__in_scout_mode:
                self.scout()
            else:
                sherlock = Book("Sherlock Holmes", "7543.bb", "Detective")
                print("Searching for {0} book".format(sherlock.get_name()))
                self.guide_user(sherlock)
                self.__in_scout_mode = True


robot = Robot()

# print(robot.organize_shelve("Biography"))
print(robot.main())
