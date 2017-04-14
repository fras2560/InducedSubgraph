'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-02
@note: contains a function to create the networkx graphs
'''
import logging
import unittest


class GraphNode():
    index = 0
    count = 0

    def __init__(self, color=None, index=None, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.color = color
        if index is None:
            index = GraphNode.index
            GraphNode.index += 1
        GraphNode.count += 1
        self.index = index

    def __eq__(self, node):
        equal = False
        try:
            if self.index == node.index:
                equal = True
        except:
            pass
        return equal

    def __copy__(self):
        return GraphNode(color=self.color,
                         index=self.index,
                         logger=self.logger)

    def __le__(self, node):
        equal = False
        try:
            if self.index <= node.index:
                equal = True
        except:
            pass
        return equal

    def __lt__(self, node):
        equal = False
        try:
            if self.index < node.index:
                equal = True
        except:
            pass
        return equal

    def __hash__(self):
        return hash(self.index)


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

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
