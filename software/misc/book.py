import yaml


class Book:
    def __init__(self, name=None, universal_code=None, category=None):
        self.__name = name
        self.__universal_code = universal_code
        self.__category = category
        self.__internal_code = self.generate_internal_code()

    def get_name(self):
        return self.__name

    def generate_internal_code(self):
        stream = open("library.yaml", "r")
        dictionary = yaml.safe_load(stream)

        for category, books in dictionary.items():
            if category == self.get_category():
                for index, book in enumerate(books):
                    if book == self.get_name():
                        return index

    def get_universal_code(self):
        return self.__universal_code

    def get_internal_code(self):
        return self.__internal_code

    def get_code(self):
        return self.__code

    def get_category(self):
        return self.__category
