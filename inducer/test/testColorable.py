'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for the clique cutset functions
'''
from inducer.colorable import valid_coloring, combine_color_clique, coloring,\
    chromatic_number, valid_split, add_list, assemble_coloring, convert_combo
from inducer.helper import make_claw, make_diamond, make_cycle, join
import unittest
import networkx as nx


class TestColorable(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testColoring(self):
        g = make_claw()
        result = coloring(g)
        self.assertEqual(2, len(result), "Coloring: Claw Case")
        g = make_diamond()
        result = coloring(g)
        self.assertEqual(3, len(result), "Coloring: Diamond Case")
        g = nx.Graph()
        g.add_node(0)
        g.add_node(1)
        result = coloring(g)
        self.assertEqual(1, len(result), "Coloring: Stable Set")

    def testColoringCritical(self):
        c5 = make_cycle(5)
        color = coloring(c5)
        self.assertEqual(len(color), 3)
        k1 = nx.Graph()
        k1.add_node(0)
        g = join(c5, k1)
        color = coloring(g)
        self.assertEqual(len(color), 4)

    def testColoringClique(self):
        g = make_cycle(3)
        color = coloring(g)
        self.assertEqual(len(color), 3)

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

    def testValidColoring(self):
        g = make_claw()
        # test invalid claw coloring
        coloring = [[0, 1, 2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid,
                         False,
                         "Valid coloring: Failed for one coloring on claw")
        coloring = [[1, 3, 2], [0]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid,
                         True,
                         "Valid coloring: Failed for valid coloring on claw")
        # test valid claw coloring
        coloring = [[0], [1, 2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid,
                         True,
                         "Valid coloring: Failed for valid coloring on claw")
        # test invalid claw coloring
        coloring = [[0, 1], [2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid,
                         False,
                         "Valid coloring: Failed for invalid coloring on claw")
        # test valid diamond coloring
        g = make_diamond()
        coloring = [[0], [1], [2, 3]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid,
                         True,
                         '''
                         Valid coloring: failed for valid coloring on diamond
                         ''')
        coloring = [[3], [2], [0, 1]]
        valid = valid_coloring(coloring, g)
        self.assertEqual(valid,
                         False,
                         '''
                         Valid coloring: failed for invalid coloring on diamond
                         ''')

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

    def testChromaticNumber(self):
        g = make_claw()
        chromatic = chromatic_number(g)
        expect = 2
        self.assertEqual(expect, chromatic, "Chromatic Number: Claw Case")
        g = make_diamond()
        chromatic = chromatic_number(g)
        expect = 3
        self.assertEqual(expect, chromatic, "Chromatic Number: Diamond Case")

    def testValidSplit(self):
        split = (4, 0)
        self.assertEqual(valid_split(split),
                         False,
                         "Valid split: True on Invalid Split")
        split = (4, 1)
        self.assertEqual(valid_split(split),
                         True,
                         "Valid split: True on Valid Split")

    def testConvertCombo(self):
        combo = (4, 1)
        conversion = convert_combo(combo)
        self.assertEqual(type(conversion),
                         list,
                         "Convert Combo: did not return list")

    def testAssembleColoring(self):
        split = [1, 2]
        combo = [1, 2, 3]
        result = assemble_coloring(combo, split)
        expect = [[3], [2, 1]]
        self.assertEqual(expect,
                         result,
                         "Assemble Coloring: unexpected result")
