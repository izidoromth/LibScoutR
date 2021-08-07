# class Book {
#   - string __name
#   - string __universal_code
#   - string __category
#   - int __internal_code

#   + string get_name()
#   + void set_internal_code()
#   + string get_universal_code()
#   + int get_internal_code()
#   + string get_category()
# }


class Book:
    def __init__(self, name=None, universal_code=None, category=None):
        self.__name = name
        self.__universal_code = universal_code
        self.__category = category
        self.__internal_code = None

    def get_name(self):
        return self.__name

    def set_internal_code(self, code):
        self.__internal_code = code

    def get_universal_code(self):
        return self.__universal_code

    def get_internal_code(self):
        return self.__internal_code

    def get_category(self):
        return self.__category
