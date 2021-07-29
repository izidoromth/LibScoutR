"""
 _     _ _     _____                 _  ______ 
| |   (_) |   /  ___|               | | | ___ \
| |    _| |__ \ `--.  ___ ___  _   _| |_| |_/ /
| |   | | '_ \ `--. \/ __/ _ \| | | | __|    / 
| |___| | |_) /\__/ / (_| (_) | |_| | |_| |\ \ 
\_____/_|_.__/\____/ \___\___/ \__,_|\__\_| \_|

"""

from library import Library
from book import Book
from lis import LIS


def filter_list_by_category(book_list, category):
    return [book for book in book_list if book.get_category() == category]


lib = Library()
# print("Path is: ", lib.find_path("Orange", "Comic Books"))

ed_sheeran = Book("Ed Sheeran", 102, "Biography")
alan_turing = Book("Alan Turing", 2, "Biography")
steve_jobs = Book("Steve Jobs", 4, "Biography")
paul_mccartney = Book("Paul McCartney", 5, "Biography")
jim_carrey = Book("Jim Carrey", 6, "Biography")
sherlock = Book("Sherlock Holmes", 7, "Detective")
lupin = Book("Lupin", 7, "Detective")

lib.add_book(ed_sheeran)
lib.add_book(alan_turing)
lib.add_book(steve_jobs)
lib.add_book(paul_mccartney)
lib.add_book(jim_carrey)
lib.add_book(sherlock)

lista = [
    sherlock,
    ed_sheeran,
    alan_turing,
    steve_jobs,
    paul_mccartney,
    jim_carrey,
    lupin,
]

lista = filter_list_by_category(lista, "Biography")
l = LIS(lista)
for sl in l:
    for book in sl:
        print(book.get_name())
    print("------")
