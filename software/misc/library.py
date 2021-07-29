from collections import defaultdict
from book import Book


class Library:
    def __init__(self):
        self.__books = []
        self.__floor_path_edges = None
        self.__categories_positions = None

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

    def update_floor_path_edges(self):
        """
        floor:
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
                "Alan Turing",
                "Ed Sheeran",
                "Steve Jobs",
                "Paul McCartney",
                "Jim Carrey",
            ],
            "Detective": ["Scooby Doo", "Sherlock Holmes", "Lupin"],
        }

        for book in self.__books:
            for category, ordered_books in lib_config.items():
                if category == book.get_category():
                    for index, book_name in enumerate(ordered_books):
                        if book_name == book.get_name():
                            book.set_internal_code(index)

    def update_library_books(self):
        ed_sheeran = Book("Ed Sheeran", "102.1x", "Biography")
        alan_turing = Book("Alan Turing", "2321.23", "Biography")
        steve_jobs = Book("Steve Jobs", "43442.aa2", "Biography")
        paul_mccartney = Book("Paul McCartney", "5453.g", "Biography")
        jim_carrey = Book("Jim Carrey", "6233.o", "Biography")
        sherlock = Book("Sherlock Holmes", "7543.bb", "Detective")
        lupin = Book("Lupin", "7542.69", "Detective")
        scooby = Book("Scooby Doo", "7543.69", "Detective")

        self.add_book(ed_sheeran)
        self.add_book(alan_turing)
        self.add_book(steve_jobs)
        self.add_book(paul_mccartney)
        self.add_book(jim_carrey)
        self.add_book(sherlock)
        self.add_book(lupin)
        self.add_book(scooby)

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
