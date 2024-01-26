'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for the dcolor class and methods
'''
from inducer.dcolor import Dcolor, combine_color_clique, convert_combo, \
    add_list
from inducer.helper import make_diamond, make_claw, make_cycle, join
import networkx as nx
import unittest


class TestDcolor(unittest.TestCase):

    def setUp(self):
        self.dcolor = Dcolor(make_claw())

    def tearDown(self):
        pass

    def testColoringAux(self):
        self.dcolor.color_aux()

    def testCreateCliqueList(self):
        c, k, i = self.dcolor.create_clique_list()
        self.assertEqual([[[0], [1]], [[2]], [[3]]], c)
        self.assertEqual(k, 2)
        self.assertEqual(i, 0)
        self.dcolor = Dcolor(make_diamond())
        c, k, i = self.dcolor.create_clique_list()
        self.assertEqual([[[0], [1], [2]], [[3]]], c)
        self.assertEqual(k, 3)
        self.assertEqual(i, 0)

    def testColor(self):
        result = self.dcolor.color()
        expect = [[0], [1, 2, 3]]
        self.assertEqual(expect, result, "Coloring: Claw Case")
        self.dcolor = Dcolor(make_diamond())
        result = self.dcolor.color()
        expect = [[0], [1], [2, 3]]
        self.assertEqual(expect, result, "Coloring: Diamond Case")
        g = nx.Graph()
        g.add_node(0)
        g.add_node(1)
        self.dcolor = Dcolor(g)
        result = self.dcolor.color()
        expect = [[0, 1]]
        self.assertEqual(expect, result, "Coloring: Stable Set")

    def testColoringCritical(self):
        self.dcolor = Dcolor(make_cycle(5))
        color = self.dcolor.color()
        expect = [[0], [1, 3], [2, 4]]
        self.assertEqual(len(color), 3)
        self.assertEqual(color, expect)
        k1 = nx.Graph()
        k1.add_node(0)
        g = join(make_cycle(5), k1)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        self.assertEqual(len(color), 4)
        expect = [[5], [0], [1, 3], [2, 4]]
        self.assertEqual(expect, color)

    def testColoringHardGraph(self):
        # C5 + 5 Xi
        g = make_cycle(5)
        index = 0
        for i in range(5, 10):
            g.add_node(i)
            # make it a two vertex
            g.add_edge(i, (index + 0) % 5)  # xi
            g.add_edge(i, (index + 1) % 5)
            index += 1
        g.add_edge(5, 6)
        g.add_edge(5, 8)
        g.add_edge(6, 8)
        g.add_edge(7, 9)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        expect = [[1, 8, 9], [5, 4, 7], [2], [0, 3, 6]]
        self.assertEqual(self.dcolor.valid_coloring(color), True)
        self.assertEqual(color, expect)
        # C5 + 2 Yi
        g = make_cycle(5)
        g.add_node(5)
        g.add_edge(0, 5)
        g.add_edge(1, 5)
        g.add_edge(2, 5)
        g.add_node(6)
        g.add_edge(0, 6)
        g.add_edge(3, 6)
        g.add_edge(4, 6)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        expect = [[0, 3], [1, 4], [5, 6], [2]]
        self.assertEqual(self.dcolor.valid_coloring(color), True)
        self.assertEqual(color, expect)

    def testColorCycle(self):
        g = make_cycle(5)
        for i in range(5, 100):
            g.add_node(i)
            g.add_edge(i - 1, i)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        self.assertEqual(len(color), 3)
        self.assertEqual(self.dcolor.valid_coloring(color), True)

    def testColoringClique(self):
        g = make_cycle(3)
        self.dcolor = Dcolor(g)
        color = self.dcolor.color()
        expect = [[0], [1], [2]]
        self.assertEqual(len(color), 3)
        self.assertEqual(color, expect)

    def testCombineColorClique(self):
        coloring = [[3], [2]]
        clique = [[0], [1]]
        expect = [
            [[0, 3], [1, 2]],
            [[1, 3], [0, 2]]
        ]
        index = 0
        for combo in combine_color_clique(clique, coloring):
            self.assertEqual(combo, expect[index])
            index += 1
        coloring = [[0, 1]]
        clique = [[2], [3]]
        expect = [
            [[2, 0, 1], [3]],
            [[2], [3, 0, 1]],
            [[3, 0, 1], [2]],
            [[3], [2, 0, 1]]
        ]
        index = 0
        for combo in combine_color_clique(clique, coloring):
            self.assertEqual(combo, expect[index])
            self.assertEqual(combo, expect[index])
            index += 1
        coloring = [[0], [1], [2]]
        clique = [[3], [4]]
        expect = [
            [[0, 3], [1, 4], [2]],
            [[0], [1, 3], [2, 4]],
            [[0, 4], [1, 3], [2]],
            [[0], [1, 4], [2, 3]]
        ]
        index = 0
        for combo in combine_color_clique(clique, coloring):
            self.assertEqual(combo, expect[index])
            index += 1

    def testAddList(self):
        l1 = [[1], [2]]
        l2 = [[3], [4, 5]]
        result = add_list(l1, l2, 0)
        expect = [[1, 3], [2, 4, 5]]
        self.assertEqual(result, expect)
        l1 = [[1], [2], [6]]
        l2 = [[3], [4, 5]]
        result = add_list(l1, l2, 0)
        expect = [[1, 3], [2, 4, 5], [6]]
        self.assertEqual(result, expect)
        result = add_list(l1, l2, 1)
        expect = [[1], [2, 3], [6, 4, 5]]
        self.assertEqual(result, expect)

    def testConvertCombo(self):
        combo = (4, 1)
        conversion = convert_combo(combo)
        self.assertEqual(type(conversion), list,
                         "Convert Combo: did not return list")
