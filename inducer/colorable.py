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

from helper import make_claw, make_diamond
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testValidColoring(self):
        nodes = [0,1,2]
        g = make_claw()
        # test valid claw coloring
        coloring = [[0], [1, 2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, True,
                         "Valid coloring: Failed for valid coloring on claw")
        # test invalid claw coloring
        coloring = [[0, 1], [2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, False,
                         "Valid coloring: Failed for invalid coloring on claw")
        # test valid diamond coloring
        g = make_diamond()
        coloring = [[0], [1], [2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, True, 
                         "Valid coloring: failed for valid coloring on diamond")
        coloring = [[3], [2], [0, 1]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid, False, 
                         "Valid coloring: failed for invalid coloring on diamond")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()