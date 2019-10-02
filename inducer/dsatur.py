'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-05
@note: coloring_aux with a greedy algorithm
'''
import logging
import unittest
import networkx as nx
from inducer.graph import available_color,\
    color_vertex,\
    copy_graph,\
    convert_to_networkx,\
    valid_coloring,\
    chromatic_number,\
    is_colored, get_color


def inducer_coloring(G):
    (H, chromatic) = coloring(G)
    colors = [[] for __ in range(0, chromatic)]
    for node in H.nodes():
        colors[get_color(H, node)].append(node)
    return colors


def coloring(G, logger=None):
    """Returns a coloring and chromatic number"""
    if logger is None:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
    H = dsatur(G, logger)
    return (H, chromatic_number(H))


def dsatur(G, logger):
    """Returns a coloring using dsatur

    Parameters:
        G: the graph to color (networkx)
        logger: the logger to use
    Returns:
        H: a colored copy of the G (networkx)
    Note:
        used the networkx implementaiton as a starting base but made changes
    """
    H = copy_graph(G)
    len_g = len(H)
    no_colored = 0
    distinct_colors = {}
    for node in H.nodes():
        distinct_colors[node] = set()
    while no_colored != len_g:
        if no_colored == 0:
            # When sat. for all nodes is 0, yield the node with highest degree
            node = max([x for x in H.nodes()],
                       key=lambda x: len(list(H.neighbors(x))))
        else:
            # want the vertex with the highest saturation
            highest_saturation = -1
            highest_saturation_nodes = []
            for node, distinct in distinct_colors.items():
                # If the node is not already colored
                if not is_colored(H, node):
                    saturation = len(distinct)
                    if saturation > highest_saturation:
                        highest_saturation = saturation
                        highest_saturation_nodes = [node]
                    elif saturation == highest_saturation:
                        highest_saturation_nodes.append(node)
            if len(highest_saturation_nodes) == 1:
                node = highest_saturation_nodes[0]
            else:
                # Return the node with highest degree
                max_node = max([x for x in highest_saturation_nodes],
                               key=lambda x: len(list(H.neighbors(x))))
                node = max_node
        color = 0
        # find some color can use for it
        while not available_color(H, node, color):
            color += 1
        # color the vertex
        color_vertex(H, node, color)
        logger.debug("Colored {} to {}".format(node, color))
        no_colored += 1
        # tells it neighbors what is up
        for neighbour in H.neighbors(node):
            distinct_colors[neighbour].add(color)
    return H


class Test(unittest.TestCase):

    def testDsaturColor(self):
        # test K3
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        G = convert_to_networkx(d)
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)
        # test cycle of size 5
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
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)
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
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)

    def testDsaturColorPeterson(self):
        G = copy_graph(nx.petersen_graph())
        (H, chromatic) = coloring(G)
        self.assertEqual(valid_coloring(H), True)
        self.assertEqual(chromatic, 3)

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

    def testDsaturColorSubOptimal(self):
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
        self.assertEqual(chromatic, 4)
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
        self.assertEqual(chromatic, 5)
