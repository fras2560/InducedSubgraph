'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for strong stable set functions
'''
from inducer.strong_stable_set import strong_stable_set, stable_set
from inducer.helper import make_clique, make_diamond, make_cycle
import networkx as nx
import unittest


class TestStrongStableSet(unittest.TestCase):

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
