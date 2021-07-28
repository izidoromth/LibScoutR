"""
 _     _ _     _____                 _  ______ 
| |   (_) |   /  ___|               | | | ___ \
| |    _| |__ \ `--.  ___ ___  _   _| |_| |_/ /
| |   | | '_ \ `--. \/ __/ _ \| | | | __|    / 
| |___| | |_) /\__/ / (_| (_) | |_| | |_| |\ \ 
\_____/_|_.__/\____/ \___\___/ \__,_|\__\_| \_|

"""

from library import Library

lib = Library()
print("We know we are on Orange and searching for a book under the Horror category")
print("Path is: ", lib.find_path("Orange", "Horror"))
# print(lib.generate_categories_edges("Adventure"))
