'''
Created on Oct 21, 2015

@author: Mobile Team
'''
from dcolor import dense_color_wrapper
from colorable import coloring as color
def critical(G, logger=None, dense=False):
    '''
    a method that finds if the graph is critical
    Parameters:
        G: the graph to check (networkx)
        logger: an optional logger
        dense: True if the graph is quite dense (boolean)
    Returns:
        K: how many colors the graphs need to be colored (int),
            None if the graph is not critical
    '''
    if dense:
        coloring = color
    else:
        coloring = dense_color_wrapper
    is_critical = True
    nodes = G.nodes()
    index = 0
    chromatic = len(coloring(G))
    while is_critical and index < len(nodes):
        g = G.copy()
        g.remove_node(nodes[index])
        check = len(coloring(g))
        if check != (chromatic -1):
            if logger is not None:
                logger.info(index)
                logger.info("G is not critical")
            is_critical = False
        index += 1
    K = None
    if is_critical:
        K = chromatic
    return K

import unittest
from inducer.helper import make_claw, make_wheel
class Tester(unittest.TestCase):
    def testCritical(self):
        self.assertEqual(critical(make_claw()), None)
        self.assertEqual(critical(make_claw(), dense=True), None)
        self.assertEqual(critical(make_wheel(6)), 4)
        self.assertEqual(critical(make_wheel(6), dense=True), 4)
        self.assertEqual(critical(make_wheel(7)), None)
