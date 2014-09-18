"""
-------------------------------------------------------
contains
holds a function contains
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
import itertools
import networkx as nx
import inducer.helper
def contains(G, H):
    '''
    contains
    a function that checks if G has an induced subgraph of H
    Parameters:
        G: the graph to check (networkx)
        H: the induced subgraph (networkx)
    Returns:
        induced: nodes of induced isomorphic graph in G
    Method:
        just create every permutation of the G graph with as many vertices
        as H and use networkx to check if isomorphic
    Note:
         not solved in polynomial time (only use for small cases)
    '''
    n = len(G)
    k = len(H)
    if n < k:
        return None
    permutations = create_permutations(n, k)
    induced = None
    for subset in permutations:
        subgraph = G.subgraph(subset)
        if nx.faster_could_be_isomorphic(subgraph, H):
            if nx.is_isomorphic(subgraph, H):
                induced = {
                           'nodes': subgraph.nodes(),
                           'edges': subgraph.edges()
                           }
                break # only want to find one
    return induced
        
def create_permutations(n, k):
    '''
    create_permutations
    a function which returns a list of all possible permutations n choose k
    Parameters:
        n: the total number of items
        k: the number of items to choose
    Returns:
        iterator: to the list of permutations
    '''
    number_list = []
    for x in range(0,n):
        number_list.append(x)
    return itertools.permutations(number_list, k)


import unittest
class tester(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testContains(self):
        h = helper.make_claw()
        g = helper.make_wheel(7)
        induced = contains(g, h)
        expected = [1, 3, 5, 6] 
        self.assertEqual(induced, expected,
                         "Contains: Failed to find a claw in W7")