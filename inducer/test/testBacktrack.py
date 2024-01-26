'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for the back tracking functions
'''
import unittest
from inducer.backtracking import forward_check, inducer_coloring, \
    least_constraining_colors, ordering_node, coloring_aux, coloring
from inducer.graph import color_vertex, \
    valid_coloring, \
    chromatic_number, \
    convert_to_networkx


class TestBacktracking(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBacktrackBasics(self):
        # test C5
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
        (colored_G, steps) = coloring_aux(G, {})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 15)

    def testBacktrackForwardCheck(self):
        # test C5
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
        forward = forward_check
        (colored_G, steps) = coloring_aux(G, {'forward_check': forward})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 13)

    def testBacktrackOrdering(self):
        # test C5
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
        next_node = ordering_node
        (colored_G, steps) = coloring_aux(G, {'next_node': next_node})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 17)

    def testBacktrackLeastConstrainingColors(self):
        # test C5
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
        lcc = least_constraining_colors
        (colored_G, steps) = coloring_aux(G, {'get_colors': lcc})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 15)

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

    def testLeastConstrainingColors(self):
        # test C5
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
        color_vertex(G, 4, 0)
        color_vertex(G, 3, 1)
        colors = least_constraining_colors(G, 1, 3)
        self.assertEqual([0, 1, 2], colors)
        color_vertex(G, 4, 0)
        color_vertex(G, 3, 1)
        color_vertex(G, 2, 0)
        colors = least_constraining_colors(G, 1, 3)
        self.assertEqual([1, 2], colors)
        # test a diamond
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
        color_vertex(G, 0, 0)
        color_vertex(G, 2, 1)
        colors = least_constraining_colors(G, 3, 3)
        self.assertEqual([0, 2], colors)

    def testForwardCheck(self):
        # test C5
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
        # there is a path forward
        forward = forward_check(G, 2)
        self.assertEqual(forward, True)
        # color both neighbors of 1 so no path forward
        color_vertex(G, 0, 0)
        color_vertex(G, 2, 1)
        forward = forward_check(G, 2)
        self.assertEqual(forward, False)
        # now expand number of colors opening up path forward
        forward = forward_check(G, 3)
        self.assertEqual(forward, True)

    def testOrderingNodeC5(self):
        # test C5
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
        node = ordering_node(G, 2)
        self.assertEqual(node, 0)
        # color vertex 0
        color_vertex(G, 0, 0)
        node = ordering_node(G, 2)
        self.assertEqual(node, 2)
        # color vertex 2
        color_vertex(G, 2, 1)
        node = ordering_node(G, 2)
        self.assertEqual(node, 3)
        # color vertex 3
        color_vertex(G, 3, 0)
        node = ordering_node(G, 2)
        self.assertEqual(node, 1)
        # color vertex 1
        color_vertex(G, 1, 2)
        node = ordering_node(G, 3)
        self.assertEqual(node, 4)
        # color vertex =4
        color_vertex(G, 4, 1)
        node = ordering_node(G, 3)
        self.assertEqual(node, None)

    def testOrderingNodeTiebreaker(self):
        # test the tiebreaker
        d = {
            "nodes": [0, 1, 2, 3, 4, 5, 6],
            "edges": [
                [0, 2],
                [0, 3],
                [0, 4],
                [1, 4],
                [1, 5],
                [1, 6],
                [3, 4],
                [4, 5],
            ]
        }
        G = convert_to_networkx(d)
        # both have the same amount of moves (so first one aka 0)
        color_vertex(G, 4, 0)
        color_vertex(G, 2, 1)
        color_vertex(G, 6, 1)
        node = ordering_node(G, 2)
        self.assertEqual(node, 0)
        # 0 has less moves
        color_vertex(G, 4, 0)
        color_vertex(G, 2, 1)
        color_vertex(G, 6, 0)
        node = ordering_node(G, 2)
        self.assertEqual(node, 0)
        # 1 has less moves
        color_vertex(G, 4, 0)
        color_vertex(G, 2, 0)
        color_vertex(G, 6, 1)
        node = ordering_node(G, 2)
        self.assertEqual(node, 1)

    def testBacktrackingColorSubOptimal(self):
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
        self.assertEqual(chromatic, 3)
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
        self.assertEqual(chromatic, 4)
