from collections import defaultdict
from book import Book
import yaml
import requests


class Library:
    def __init__(self):
        self.__books = []
        self.__floor_path_edges = None
        self.__categories_positions = None
        self.__scout_path = None
        self.__path_positions = None
        self.__config_filename = "libconfig.yaml"

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

    def generate_book_from_json(self, book_json):
        book = Book(
            book_json["name"],
            book_json["universal_code"],
            book_json["current_category"],
        )
        return book

    def setup(self):
        self.update_library_books()
        self.update_books_internal_code()
        self.update_categories_positions()
        self.update_floor_path_edges()
        self.update_scout_path()
        self.update_path_positions()

    def get_scout_path(self):
        return list(self.__scout_path)

    def update_scout_path(self):
        with open(self.__config_filename) as f:
            config = yaml.safe_load(f)
            self.__scout_path = config["Scout Path"]

    def update_path_positions(self):
        with open(self.__config_filename) as f:
            config = yaml.safe_load(f)
            self.__path_positions = config["Path Position"]

    def get_path_positions(self):
        return self.__path_positions

    def update_floor_path_edges(self):
        """
        floor colored tags:
        ORANGE-------------RED---------------BLUE
        |                   |                   |
        |                   |                   |
        |                   |                   |
        BROWN------------PURPLE------------YELLOW
        """
        with open(self.__config_filename) as f:
            config = yaml.safe_load(f)
            self.__floor_path_edges = config["Path Edges"]

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
        # {
        #   '1st floor': {
        #       'Adventure': ['Orange', 'Red'],
        #       'Comic Books': ['Red', 'Blue'],
        #       'Detective': ['Brown', 'Purple'],
        #       'Horror': ['Purple', 'Yellow']
        #   },
        #   '2nd floor': {
        #       'Romance': ['Orange', 'Red'],
        #       'Science Fiction': ['Red', 'Blue'],
        #       'Suspense': ['Brown', 'Purple'],
        #       'Biography': ['Purple', 'Yellow']
        #   }
        # }
        with open(self.__config_filename) as f:
            config = yaml.safe_load(f)
            self.__categories_positions = config["Categories Positions"]

    def update_books_internal_code(self):
        lib_config = requests.get("http://192.168.0.11:5001/ordered_books").json()
        # lib_config = {
        #     "Romance": [
        #         "823 O79mi 0070",  # Alan Turing
        #         "823 D754vt 0071",  # Steve Jobs
        #         "823 D314r 0072",  # Ed Sheeran
        #         "823 D754en 0073",  # Paul McCartney
        #         "823 D754en 0074",  # Paul McCartney
        #     ]
        # }
        print(lib_config)

        for book in self.__books:
            for category, ordered_books in lib_config.items():
                if category == book.get_category():
                    for index, book_code in enumerate(ordered_books):
                        if book_code == book.get_universal_code():
                            book.set_internal_code(index)

    def update_library_books(self):
        # books = []
        books = requests.get("http://192.168.0.11:5001/robot_books").json()

        # books = [
        #     {"name": "Ed Sheeran", "ucode": "823 O79mi 0070", "category": "Romance"},
        #     {"name": "Alan Turing", "ucode": "823 D314r 0072", "category": "Romance"},
        #     {"name": "Steve Jobs", "ucode": "823 D754vt 0071", "category": "Romance"},
        #     {"name": "Paul McCartney", "ucode": "823 D754en 0073", "category": "Romance"},
        # ]

        print(books)        

        for book in books:
            self.add_book(Book(book["name"], book["ucode"], book["category"]))

    def get_category_position(self, category):
        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                if key == category:
                    return [value[0], value[1]]

    def get_categories_from_color_position(self, start_color, end_color):
        at_categories = {}
        for floor, categories in self.__categories_positions.items():
            for category, position in categories.items():
                if position == [start_color, end_color] or position == [
                    end_color,
                    start_color,
                ]:
                    at_categories[floor] = category
        return at_categories
        # {
        #   '1st floor': {
        #       'Adventure': ['Orange', 'Red'],
        #       'Comic Books': ['Red', 'Blue'],
        #       'Detective': ['Brown', 'Purple'],
        #       'Horror': ['Purple', 'Yellow']
        #   },
        #   '2nd floor': {
        #       'Romance': ['Orange', 'Red'],
        #       'Science Fiction': ['Red', 'Blue'],
        #       'Suspense': ['Brown', 'Purple'],
        #       'Biography': ['Purple', 'Yellow']
        #   }
        # }

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

                        # Remove first node (start node)
                        new_path.pop(0)
                        return new_path

                explored.append(node)

        # Condition when the nodes
        # are not connected
        print("So sorry, but a connecting path doesn't exist :(")
        return list()


# lib = Library()
# lib.setup()
# print(lib.find_path("Orange", "Blue"))
