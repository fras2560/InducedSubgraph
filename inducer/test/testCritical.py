'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for the critical function
'''
from inducer.critical import critical
from inducer.helper import make_claw, make_wheel
import unittest


class TestCritical(unittest.TestCase):

    def testCritical(self):
        self.assertEqual(critical(make_claw()), None)
        self.assertEqual(critical(make_claw(), dense=True), None)
        self.assertEqual(critical(make_wheel(6)), 4)
        self.assertEqual(critical(make_wheel(6), dense=True), 4)
        self.assertEqual(critical(make_wheel(7)), None)
