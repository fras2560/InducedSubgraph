'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for ISK4Free and its methods
'''
from inducer.isk4 import ISK4Free
from inducer.helper import make_co_twin_c5, make_cycle, make_clique
from inducer.container import induced_subgraph
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def compare_graphs(self, g, h):
        same = False
        if (len(g.nodes()) == len(h.nodes())):
            induced = induced_subgraph(g, h)
            if induced is not None:
                same = True
        return same

    def testCreateSubdivision(self):
        g = ISK4Free(make_co_twin_c5())
        result = g.create_subdivions([0, 0, 0, 0, 0, 0])
        self.assertEqual(self.compare_graphs(result, make_clique(4)), True)
        result = g.create_subdivions([1, 0, 0, 0, 0, 0])
        expect = make_clique(4)
        expect.remove_edge(2, 3)
        expect.add_node(4)
        expect.add_edge(2, 4)
        expect.add_edge(3, 4)
        self.assertEqual(self.compare_graphs(result, expect), True)

    def testFree(self):
        # simple case
        g = ISK4Free(make_clique(4))
        result = g.free()
        self.assertEqual(self.compare_graphs(result, make_clique(4)), True)
        # another simple case
        g = ISK4Free(make_co_twin_c5())
        result = g.free()
        expect = make_co_twin_c5()
        self.assertEqual(self.compare_graphs(result, expect), True)
        # difficult graph
        graph = make_cycle(5)
        graph.add_node(5)
        graph.add_edge(0, 5)
        graph.add_edge(1, 5)
        graph.add_edge(3, 5)
        g = ISK4Free(graph)
        result = g.free()
        self.assertEqual(self.compare_graphs(result, graph), True)
        # one with no ISK4
        graph = make_cycle(6)
        g = ISK4Free(graph)
        result = g.free()
        self.assertEqual(result, None)
