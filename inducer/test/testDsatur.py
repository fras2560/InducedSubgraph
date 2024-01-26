'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for the dsatur coloring function and helper functions
'''
from inducer.dsatur import coloring, inducer_coloring
from inducer.graph import copy_graph, \
    convert_to_networkx, \
    valid_coloring
import unittest
import networkx as nx


class TestDsatur(unittest.TestCase):

    def testDsaturColor(self):
        # test K3
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        G = convert_to_networkx(d)
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)
        # test cycle of size 5
        d = {
            "nodes": [0, 1, 2, 3, 4],
            "edges": [
                [0, 1],
                [0, 4],
                [1, 2],
                [2, 3],
                [3, 4]
            ]
        }
        G = convert_to_networkx(d)
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)
        # test diamond
        d = {
            "nodes": [0, 1, 2, 3],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2],
                [1, 3],
                [2, 3]
            ]
        }
        G = convert_to_networkx(d)
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)

    def testDsaturColorPeterson(self):
        G = copy_graph(nx.petersen_graph())
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)

    def testInducerColoring(self):
        # test diamond
        d = {
            "nodes": [0, 1, 2, 3],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2],
                [1, 3],
                [2, 3]
            ]
        }
        G = convert_to_networkx(d)
        H = inducer_coloring(G)
        self.assertEqual([[1], [2], [0, 3]], H)

    def testDsaturColorSubOptimal(self):
        # test cycle of size 5
        d = {
            "nodes": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            "edges": [
                [0, 1],
                [0, 4],
                [1, 2],
                [2, 3],
                [3, 4],
                [0, 5],
                [1, 5],
                [2, 5],
                [0, 6],
                [3, 6],
                [4, 6],
                [1, 7],
                [1, 8],
                [2, 9],
                [2, 10],
                [3, 11],
                [3, 12],
                [4, 13],
                [4, 14],
            ]
        }
        G = convert_to_networkx(d)
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 4)
        # some graph i found that dasatur does not do well on
        # it looks like two connected diamonds but one diamond is rotated
        # http://www.sciencedirect.com/science/article/pii/S0012365X00004398
        d = {
            "nodes": [0, 1, 2, 3, 4, 5, 6, 7],
            "edges": [
                [0, 1],
                [0, 2],
                [0, 3],
                [0, 4],
                [1, 3],
                [2, 3],
                [3, 7],
                [4, 5],
                [4, 6],
                [5, 6],
                [5, 7],
                [6, 7]
            ]
        }
        G = convert_to_networkx(d)
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 4)
        # same as above but with a join vertex to each diamond
        d = {
            "nodes": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "edges": [
                [0, 1],
                [0, 2],
                [0, 3],
                [0, 4],
                [1, 3],
                [2, 3],
                [3, 7],
                [4, 5],
                [4, 6],
                [5, 6],
                [5, 7],
                [6, 7],
                [8, 0],
                [8, 1],
                [8, 2],
                [8, 3],
                [9, 4],
                [9, 5],
                [9, 6],
                [9, 7]
            ]
        }
        G = convert_to_networkx(d)
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 5)
