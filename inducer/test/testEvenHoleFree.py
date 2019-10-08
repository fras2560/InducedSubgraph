'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for even hole free functions
'''
from inducer.EvenHoleFree import even_hole_free, odd_hole_free
from inducer.helper import make_cycle
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEvenHoleFree(self):
        g = make_cycle(4)
        self.assertEqual(even_hole_free(g).edges(), g.edges())
        self.assertEqual(even_hole_free(g).nodes(), g.nodes())
        g = make_cycle(5)
        self.assertEqual(even_hole_free(g), None)
        g = make_cycle(10)
        self.assertEqual(even_hole_free(g).edges(), g.edges())
        self.assertEqual(even_hole_free(g).nodes(), g.nodes())

    def testOddHoleFree(self):
        g = make_cycle(4)
        self.assertEqual(odd_hole_free(g), None)
        g = make_cycle(5)
        self.assertEqual(odd_hole_free(g).edges(), g.edges())
        self.assertEqual(odd_hole_free(g).nodes(), g.nodes())
        g = make_cycle(10)
        self.assertEqual(odd_hole_free(g), None)
        g = make_cycle(11)
        self.assertEqual(odd_hole_free(g).edges(), g.edges())
        self.assertEqual(odd_hole_free(g).nodes(), g.nodes())
