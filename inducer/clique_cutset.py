"""
-------------------------------------------------------
clique_cutset
a  function that checks if a graph has a clique cutset
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2015-10-21
-------------------------------------------------------
"""
from networkx import is_connected, find_cliques
from itertools import combinations


def clique_cutset(G):
    '''
    a function that finds a clique cutset
    Parameters:
        G: the graph to check (networx)
    Returns:
        result: None if no clique cutset, otherwise the clique which
                forms the cutset
    '''
    result = None
    cliques = find_cliques(G)
    for clique in cliques:
        # iterate through each subset of the clique
        for small_clique in subset(clique):
            g = G.copy()
            for node in small_clique:
                g.remove_node(node)
        # check if graph is connected
            if len(g.nodes()) == 0 or not is_connected(g):
                result = G.subgraph(small_clique)
                break
    return result


def subset(clique):
    '''
    a generator which yields all subset of a clique
    Parameters:
        clique: the clique to find all sub clique (list)
    Yields:
        x: the sub clique (tuple)
    '''
    for i in range(1, len(clique) + 1):
        for x in combinations(clique, i):
            yield x

import unittest
from inducer.helper import make_clique, make_diamond, make_cycle, make_kite,\
    make_bridge
import networkx as nx


class Test(unittest.TestCase):

    def testCliqueCutset(self):
        # no cutset
        result = clique_cutset(make_cycle(5))
        self.assertEqual(result, None)
        # cutset is subclique of the maximal clique
        result = clique_cutset(make_diamond())
        self.assertEqual(result.nodes(), make_clique(2).nodes())
        self.assertEqual(result.edges(), make_clique(2).edges())

        # just a normal cutset
        g = nx.Graph()
        g.add_node(2)
        result = clique_cutset(make_kite())
        self.assertEqual(result.nodes(), g.nodes())
        # whole graph is a clique
        result = clique_cutset(make_clique(4))
        self.assertEqual(result.nodes(), make_clique(4).nodes())
        self.assertEqual(result.edges(), make_clique(4).edges())
        # a random graph
        result = clique_cutset(make_bridge())
        self.assertEqual(result.nodes(), make_clique(2).nodes())
        self.assertEqual(result.edges(), make_clique(2).edges())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
