from collections import defaultdict
from book import Book


# class Library {
#   - list __books
#   - list __floor_path_edges
#   - json __categories_positions
#   - list __scout_path

#   - list __fix_path_first_node()
#   - list __fix_path_last_node()
#   - list __generate_categories_edges()
#   - list __build_graph()
#   + void setup()
#   + list get_scout_path()
#   + void update_scout_path()
#   + void update_floor_path_edges()
#   + void update_categories_positions()
#   + void update_books_internal_code()
#   + void update_library_books()
#   + list get_category_position()
#   + Book get_book_from_code()
#   + list how_a_category_should_be()
#   + list create_book_list_from_code_list()
#   + list filter_book_list_by_category()
#   + list get_books()
#   + void add_book()
#   + list get_floor_edges()
#   + list get_colors()
#   + bool edge_has_books()
#   + list get_categories()
#   + void find_path()
# }


class Library:
    def __init__(self):
        self.__books = []
        self.__floor_path_edges = None
        self.__categories_positions = None
        self.__scout_path = None

    def __fix_path_first_node(self, path, category):
        path.pop(0)
        color_to_be_added = None

        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                if key == category:
                    for color in value:
                        if color != path[0]:
                            color_to_be_added = color

        path.insert(0, color_to_be_added)
        return path

    def __fix_path_last_node(self, path, category):
        path.pop()
        color_to_be_added = None

        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                if key == category:
                    for color in value:
                        if color != path[-1]:
                            color_to_be_added = color

        path.append(color_to_be_added)
        return path

    def __generate_categories_edges(self, category):
        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                if key == category:
                    return [[value[0], key], [key, value[1]]]

    def __build_graph(self, edges):
        graph = defaultdict(list)

        # Loop to iterate over every edge of the graph
        for edge in edges:
            a, b = edge[0], edge[1]

            # Creating the graph as adjacency list
            graph[a].append(b)
            graph[b].append(a)
        return graph

    def setup(self):
        self.update_library_books()
        self.update_books_internal_code()
        self.update_categories_positions()
        self.update_floor_path_edges()
        self.update_scout_path()

    def get_scout_path(self):
        return self.__scout_path

    def update_scout_path(self):
        scout_path = ["Orange", "Red", "Blue", "Yellow", "Purple", "Brown"]
        self.__scout_path = scout_path

    def update_floor_path_edges(self):
        """
        floor colored tags:
        ORANGE-------------RED---------------BLUE
        |                   |                   |
        |                   |                   |
        |                   |                   |
        BROWN------------PURPLE------------YELLOW
        """

        path_edges = [
            ["Orange", "Red"],
            ["Orange", "Brown"],
            ["Red", "Blue"],
            ["Red", "Purple"],
            ["Brown", "Purple"],
            ["Purple", "Yellow"],
            ["Blue", "Yellow"],
        ]
        self.__floor_path_edges = path_edges

    def update_categories_positions(self):
        """
        1st row:
        ------Adventure----------Comic Books-----
        |                   |                   |
        |                   |                   |
        |                   |                   |
        ------Detective-------------Horror-------

        2nd row:
        ------Romance----------Science Fiction---
        |                   |                   |
        |                   |                   |
        |                   |                   |
        ------Suspense------------Biography------
        """

        categories = {
            "1st floor": {
                "Adventure": ["Orange", "Red"],
                "Comic Books": ["Red", "Blue"],
                "Detective": ["Brown", "Purple"],
                "Horror": ["Purple", "Yellow"],
            },
            "2nd floor": {
                "Romance": ["Orange", "Red"],
                "Science Fiction": ["Red", "Blue"],
                "Suspense": ["Brown", "Purple"],
                "Biography": ["Purple", "Yellow"],
            },
        }
        self.__categories_positions = categories

    def update_books_internal_code(self):
        lib_config = {
            "Biography": [
                "2321.23",  # Alan Turing
                "102.1x",  # Ed Sheeran
                "43442.aa2",  # Steve Jobs
                "5453.g",  # Paul McCartney
                "6233.o",  # Jim Carrey
            ],
            "Detective": [
                "7543.69",  # Scooby Doo
                "7543.bb",  # Sherlock Holmes
                "7542.69",  # Lupin
            ],
        }

        for book in self.__books:
            for category, ordered_books in lib_config.items():
                if category == book.get_category():
                    for index, book_code in enumerate(ordered_books):
                        if book_code == book.get_universal_code():
                            book.set_internal_code(index)

    def update_library_books(self):
        books = [
            {"name": "Ed Sheeran", "ucode": "102.1x", "category": "Biography"},
            {"name": "Alan Turing", "ucode": "2321.23", "category": "Biography"},
            {"name": "Steve Jobs", "ucode": "43442.aa2", "category": "Biography"},
            {"name": "Paul McCartney", "ucode": "5453.g", "category": "Biography"},
            {"name": "Jim Carrey", "ucode": "6233.o", "category": "Biography"},
            {"name": "Sherlock Holmes", "ucode": "7543.bb", "category": "Detective"},
            {"name": "Lupin", "ucode": "7542.69", "category": "Detective"},
            {"name": "Scooby Doo", "ucode": "7543.69", "category": "Detective"},
        ]

        for book in books:
            self.add_book(Book(book["name"], book["ucode"], book["category"]))

    def get_category_position(self, category):
        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                if key == category:
                    return [value[0], value[1]]

    def get_book_from_code(self, code):
        for book in self.__books:
            if book.get_universal_code() == code:
                return book

    def how_a_category_should_be(self, category):
        books = [book for book in self.__books if book.get_category() == category]
        books = sorted(books, key=lambda book: book.get_code())
        return [book for book in books]

    def create_book_list_from_code_list(self, code_list):
        result = []
        for code in code_list:
            book = self.get_book_from_code(code)
            if book:
                result.append(book)
        return result

    def filter_book_list_by_category(self, book_list, category):
        return [book for book in book_list if book.get_category() == category]

    def get_books(self):
        return self.__books

    def add_book(self, book):
        self.__books.append(book)

    def get_floor_edges(self):
        return self.__floor_path_edges

    def get_colors(self):
        colors = set()
        for edge in self.__floor_path_edges:
            for color in edge:
                colors.add(color)

        return colors

    def edge_has_books(self, edge):
        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                if set(value) == set(edge):
                    return True

        return False

    def get_categories(self):
        categories = set()
        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                categories.add(key)

        return categories

    def find_path(self, start_category_or_color, goal_category_or_color):
        edges = self.__floor_path_edges

        if start_category_or_color in self.get_categories():
            edges.extend(self.__generate_categories_edges(start_category_or_color))
            start_node_is_category = True
        else:
            start_node_is_category = False

        if goal_category_or_color in self.get_categories():
            edges.extend(self.__generate_categories_edges(goal_category_or_color))
            goal_node_is_category = True
        else:
            goal_node_is_category = False

        graph = self.__build_graph(edges)

        explored = []
        # Queue for traversing the
        # graph in the BFS
        queue = [[start_category_or_color]]

        # If the desired node is
        # reached
        if start_node_is_category and goal_node_is_category:
            if set(self.get_category_position(start_category_or_color)) == set(
                self.get_category_position(goal_category_or_color)
            ):
                print("Same Node")
                return list()
        if start_category_or_color == goal_category_or_color:
            print("Same Node")
            return list()

        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]

            # Condition to check if the
            # current node is not visited
            if node not in explored:
                neighbours = graph[node]

                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    # Condition to check if the
                    # neighbour node is the goal
                    if neighbour == goal_category_or_color:
                        if goal_node_is_category:
                            new_path = self.__fix_path_last_node(
                                new_path, goal_category_or_color
                            )
                        if start_node_is_category:
                            new_path = self.__fix_path_first_node(
                                new_path, start_category_or_color
                            )

                        return new_path

                explored.append(node)

        # Condition when the nodes
        # are not connected
        print("So sorry, but a connecting path doesn't exist :(")
        return list()
