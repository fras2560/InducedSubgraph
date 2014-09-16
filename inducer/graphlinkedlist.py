"""
-------------------------------------------------------
graphlinkedlist
data structure for graph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-16
-------------------------------------------------------
"""
class AdjacencyListNode():
    def __init__(self, vertex=None):
        self.next = None
        self.vertex = vertex

    def insertNode(self, vertex):
        pointer = self.next
        previous = None
        while pointer != None:
            previous = pointer
            pointer = pointer.next
        if previous is None:
            self.next = AdjacencyListNode(vertex)
        else:
            previous.next = AdjacencyListNode(vertex)

class AdjacencyList():
    def __init__(self):
        self.first_vertex = None

    def __len__(self):
        pointer = self.first_vertext
        counter = 0
        while pointer is None:
            counter += 1
            pointer = pointer.next
        return counter

class GraphLinkedList():
    def __init__(self, vertices=None, ):
        self.vertices = []
        if vertices is None:
            self.number = 0
        else:
            self.number = len(vertices)

    def insert_vertex(self):
        new_vertex = AdjacencyList()
        self.vertices.append(new_vertex)

    def insert_adjacency(self,a, b):
        new_adjacent = AdjacencyListNode(b)
        new_adjacent.next = self.vertices[a].first_vertex
        self.vertices[a].first_vertex = new_adjacent

    def are_ajacent(self, a, b):
        current = self.vertices[a].first_vertex
        while current != None and current.vertex != b:
            current = current.next
        adjacent = False
        if current is not None:
            adjacent = True
        return adjacent