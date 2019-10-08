'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for the clique cutset methods
'''
from inducer.clique_cutset import clique_cutset
from inducer.helper import make_clique, make_diamond, make_cycle, make_kite,\
    make_bridge
import unittest
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
