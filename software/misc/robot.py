from library import Library


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
        self.__last_color_seen = None
        self.__current_category = None
        self.__library = Library()
        self.__library.setup()

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

    def goto(self):
        print("Path is:")
        path = self.__library.find_path("Horror", "Biography")
        return path


robot = Robot()

print(robot.organize_shelve("Biography"))
print(robot.goto())
