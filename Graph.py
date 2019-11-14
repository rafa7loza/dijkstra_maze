from math import inf


class Node:
    def __init__(self, w, destination):
        self.weight = w
        self.destination = destination


class Graph:
    def __init__(self, nodes):
        self.__nodes = nodes
        self.__adjacent_matrix = [[0 for i in range(nodes)] for j in range(nodes)]

    def __str__(self):
        s = ""
        for row in self.__adjacent_matrix:
            s += str(row) + '\n'
        return s

    def add_edge(self, source, destination, w):
        self.__adjacent_matrix[source][destination] = w

    # Auxiliary private function for the dijsktra algorithm
    def __min_distance(self, distance, spt_set):
        minimum = inf
        min_index = 0

        for v in range(self.__nodes):
            if distance[v] < minimum and not spt_set[v]:
                minimum = distance[v]
                min_index = v

        return min_index

    def __get_path(self, nodes):
        shortest_path = [nodes[-1]]

        for node in nodes[-1::-1]:
            if node[1] == shortest_path[-1][0]:
                shortest_path.append(node)
        # print(shortest_path[::-1])
        return shortest_path[::-1]

    def dijsktra(self, source, destination):
        """
        :param source: Source vertex
        :param destination: Destination Vertex
        :return: A list representing the shortest path from source to destination,
        every element of the list contains three elements (u, v, w) which represents
        the distance (w) from vertex u to v
        """
        distance = [inf for i in range(self.__nodes)]
        distance[source] = 0
        spt_set = [False for i in range(self.__nodes)]
        visited_nodes = []

        for i in range(self.__nodes):

            u = self.__min_distance(distance, spt_set)
            spt_set[u] = True
            _v = -1
            for v in range(self.__nodes):
                new_distance = distance[u] + self.__adjacent_matrix[u][v]
                if self.__adjacent_matrix[u][v] > 0 and not spt_set[v] and distance[v] > new_distance:
                    distance[v] = new_distance
                    _v = v
                    visited_nodes.append([u, _v, distance[_v]])
                    # print(u, _v, distance[_v])
                if distance[destination] != inf:
                    # print(_v, u, distance[_v])
                    path = self.__get_path(visited_nodes)
                    # print(distance[destination])
                    return path

        # print(distance[destination])
        path = self.__get_path(visited_nodes)
        return distance


def main():
    g = Graph(9)
    m = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
        [4, 0, 8, 0, 0, 0, 0, 11, 0],
        [0, 8, 0, 7, 0, 4, 0, 0, 2],
        [0, 0, 7, 0, 9, 14, 0, 0, 0],
        [0, 0, 0, 9, 0, 10, 0, 0, 0],
        [0, 0, 4, 14, 10, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 1, 6],
        [8, 11, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 2, 0, 0, 0, 6, 7, 0]]

    for i in range(len(m)):
        for j in range(len(m[0])):
            g.add_edge(i, j, m[i][j])

    print(g)
    path = g.dijsktra(0, 4)
    print(path)


if __name__ == "__main__":
    main()
