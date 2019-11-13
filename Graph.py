class Node:
    def __init__(self, w, destination):
        self.weight = w
        self.destination = destination

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adjacent_list = [[] for node in nodes]

    def addEdge(self, source, destination, w):
        pass
# https://www.tutorialspoint.com/Dijkstra-s-Algorithm-for-Adjacency-List-Representation
