'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for graph node object
'''
from inducer.graph.graph_node import GraphNode
import unittest


class TestGraphNode(unittest.TestCase):

    def setUp(self):
        GraphNode.index = 0
        GraphNode.count = 0

    def testInit(self):
        GraphNode()
        GraphNode(color=1, index=1)
        self.assertEqual(GraphNode.index, 1)
        self.assertEqual(GraphNode.count, 2)

    def testComparison(self):
        n1 = GraphNode()
        n2 = GraphNode()
        self.assertEqual(n1 < n2, True)
        self.assertEqual(n1 <= n2, True)
        self.assertEqual(n1 == n2, False)
        self.assertEqual(n1 > n2, False)
        self.assertEqual(n1 >= n2, False)
        self.assertEqual(n1 != n2, True)
        self.assertEqual(n2 == GraphNode(index=1), True)

    def testHash(self):
        self.assertEqual(hash(GraphNode()), 0)
        self.assertEqual(hash(GraphNode()), 1)
