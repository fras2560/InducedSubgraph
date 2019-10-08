'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for the container functions
'''
from inducer.helper import make_cycle, make_claw, make_co_claw,\
    make_diamond, make_co_diamond, make_wheel
from inducer.container import induced_subgraph, k_vertex
import unittest


class TestContainer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInducedSubgraph(self):
        h = make_claw()
        g = make_wheel(7)
        induced = induced_subgraph(g, h)
        expected = [0, 2, 4, 6]
        self.assertEqual(list(induced.nodes()), expected,
                         "Contains: Failed to find a claw in W7")

    def testC7CoClawClawFree(self):
        g = make_cycle(7)
        subgraphs = [make_claw(), make_co_claw()]
        k_vertexes = k_vertex(g, subgraphs)
        for index, k in enumerate(k_vertexes):
            if index > 0:
                self.assertEqual(k['has_k_vertex'], False,
                                 '''
                                 K Vertex says (claw,co-claw)-free Graph
                                 has a %s-vertex''' % index)
            else:
                self.assertEqual(k['has_k_vertex'], True,
                                 '''
                                 K Vertex says (claw,co-claw)-free Graph
                                 has no a %s-vertex''' % index)

    def testC5DiamondCoDiamondFree(self):
        g = make_cycle(5)
        subgraphs = [make_diamond(), make_co_diamond()]
        k_vertexes = k_vertex(g, subgraphs)
        expect = [False, False, True, True, False, False]
        for index, k in enumerate(k_vertexes):
            self.assertEqual(k['has_k_vertex'], expect[index],
                             '''K Vertex says (diamond,co-diamond)- free Graph
                             %d - vertex:%r but should be %r'''
                             % (index, k['has_k_vertex'], expect[index]))
        set_2_vertex = [(0, 1), (0, 4), (1, 2), (2, 3), (3, 4)]
        for check in set_2_vertex:
            self.assertEqual(check in k_vertexes[2]['combinations'], True,
                             '''
                            K vertex missing 2 Vertex set (%d, %d)
                            on (diamond, co-diamond)-free Grpah
                            ''' % (check[0], check[1]))
        set_3_vertex = [(0, 1, 3),
                        (0, 2, 3),
                        (0, 2, 4),
                        (1, 2, 4),
                        (1, 3, 4)]
        for check in set_3_vertex:
            self.assertEqual(check in k_vertexes[3]['combinations'], True,
                             '''
                            K vertex missing 3 Vertex set (%d, %d, %d)
                            on (diamond, co-diamond)-free Grpah
                            ''' % (check[0], check[1], check[2]))
