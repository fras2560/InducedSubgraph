"""
-------------------------------------------------------
This program analyzes (C4,C5,4K1)-free graphs.

We are primarily interested in which graphs from this class
contains a strong stable set which meets all the maximal 
cliques of the graph in question. If no such strong stable
set exists, we wonder if the chromatic number is equal
to the ceiling of n/3.
-------------------------------------------------------
Author:  Tom LaMantia, Dallas Fraser
Email:   lama3790@mylaurier.ca, fras2560@mylaurier.ca
Version: 2015-10-21
-------------------------------------------------------
"""
from networkx import find_cliques, maximal_independent_set, graph_clique_number
from networkx.exception import NetworkXUnfeasible
from networkx import complement

def strong_stable_set(G):
    '''
    
    '''
    clique = graph_clique_number(G)
    result = None
    for stable in stable_set(G):
        g = G.copy()
        for node in stable:
            g.remove_node(node)
        if clique != graph_clique_number(g):
            result = G.subgraph(stable)
            break;
    return result

def stable_set(G):
    co_g = complement(G)
    for clique in find_cliques(co_g):
        yield clique

import unittest
from inducer.helper import make_clique, make_diamond, make_cycle
import networkx as nx
class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testStableSet(self):
        expect = [[0], [1], [2, 3]]
        for i in stable_set(make_diamond()):
            self.assertEqual(i in expect, True)

    def testStrongStableSet(self):
        g = nx.Graph()
        g.add_node(0)
        # check a triangle
        result = strong_stable_set(make_clique(3))
        self.assertEqual(result.nodes(), g.nodes())
        # check a diamond
        result = strong_stable_set(make_diamond())
        self.assertEqual(result.nodes(), g.nodes())
        # C5
        result = strong_stable_set(make_cycle(5))
        self.assertEqual(result, None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()