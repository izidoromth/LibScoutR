from collections import defaultdict


"""
floor:
ORANGE-------------RED---------------BLUE
|                   |                   |
|                   |                   |
|                   |                   |
BROWN------------PURPLE------------YELLOW


1st floor:
------Adventure----------Comic Books-----
|                   |                   |
|                   |                   |
|                   |                   |
------Detective-------------Horror-------


2nd floor:
------Romance----------Science Fiction---
|                   |                   |
|                   |                   |
|                   |                   |
------Suspense------------Biographies----

"""


class Library:
    def __init__(self):
        self.books = []
        self.order_shelves_by = "name"

        self.__floor_path_edges = [
            ["Orange", "Red"],
            ["Orange", "Brown"],
            ["Red", "Blue"],
            ["Red", "Purple"],
            ["Brown", "Purple"],
            ["Purple", "Yellow"],
            ["Blue", "Yellow"],
        ]

        self.__categories_positions = {
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
                "Biographies": ["Purple", "Yellow"],
            },
        }

    def add_book(self, book):
        self.books.append(book)

    def fix_path_last_node(self, path, category):
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

    def generate_categories_edges(self, category):
        for key, value in self.__categories_positions.items():
            for key, value in value.items():
                if key == category:
                    return [[value[0], key], [key, value[1]]]

    def build_graph(self, edges):
        graph = defaultdict(list)

        # Loop to iterate over every edge of the graph
        for edge in edges:
            a, b = edge[0], edge[1]

            # Creating the graph as adjacency list
            graph[a].append(b)
            graph[b].append(a)
        return graph

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

    def find_path(self, start_color, goal_category_or_color):
        edges = self.__floor_path_edges

        # if start_category in self.get_categories():
        #     edges.extend(self.generate_categories_edges(start_category))
        if goal_category_or_color in self.get_categories():
            edges.extend(self.generate_categories_edges(goal_category_or_color))
            goal_category_is_color = False
        else:
            goal_category_is_color = True

        graph = self.build_graph(edges)

        explored = []
        # Queue for traversing the
        # graph in the BFS
        queue = [[start_color]]

        # If the desired node is
        # reached
        if start_color == goal_category_or_color:
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
                        if goal_category_is_color:
                            return new_path
                        else:
                            return self.fix_path_last_node(
                                new_path, goal_category_or_color
                            )
                explored.append(node)

        # Condition when the nodes
        # are not connected
        print("So sorry, but a connecting path doesn't exist :(")
        return list()
