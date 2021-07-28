class Book:
    def __init__(self, name=None, code=None, category=None):
        self.__name = name
        self.__code = code
        self.__category = category

    def get_name(self):
        return self.__name

    def get_code(self):
        return self.__code

    def get_category(self):
        return self.__category
