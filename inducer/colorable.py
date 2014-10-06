"""
-------------------------------------------------------
colorable
a module to determine the chromatic number of a graph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
import unittest
import networkx as nx
from itertools import permutations

def valid_coloring(coloring, G):
    '''
    a function that determines if the coloring is valid
    Parameters:
        coloring: a list of colors in which each color is a list of nodes 
                  e.g. [[1,2],[3]]
        G: a networkx graph (networkx)
    Returns:
        valid: True if valid coloring,
               False otherwise
    '''
    valid = True
    for color in coloring:
        for vertex in color:
            neighbors = G.neighbors(vertex)
            for neighbor in neighbors:
                if neighbor in color:
                    valid = False
                    break;
            if not valid:
                break;
        if not valid:
            break;
    return valid

def color_permutations(nodes, baskets):
    '''
    a function that returns a iterator for all the possible ways to split the
    nodes into number of baskets
    Parameters:
        nodes: the list of nodes (order does matter)
        baskets: the number of baskets available (int)
    Returns:
        iterator: of all the combinations
    '''
    # TODO
    pass

def chromatic_number(G):
    '''
    a function that finds the chromatic number of graph G
    using brute force
    Parameters:
        G: the networkx graph (networkx)
    Returns:
        chromatic: the chromatic number (int)
    '''
    chromatic = 0
    valid = False
    nodes = G.nodes()
    while not valid:
        chromatic += 1
        for combo in permutations(nodes):
            for coloring in color_permutations(combo, chromatic):
                if valid_coloring(coloring, G):
                    valid = True
                    break;
            if valid:
                break
    return chromatic

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()