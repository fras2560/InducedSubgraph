'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for graph and their functions
'''
from inducer.graph import available_color, create_graph, convert_to_d3,\
    convert_to_networkx, d3_to_text, text_to_d3, available_colors, copy_graph,\
    valid_coloring, color_vertex
import networkx as nx
import unittest


class testGraph(unittest.TestCase):

    def failing_test(self):
        self.assertEqual(True, False)

    def graph_equal(self, g1, g2):
        equal = True
        for n1 in g1.nodes():
            if n1 not in g2.nodes():
                equal = False
                break
        if equal:
            for edge in g1.edges():
                if edge not in g2.edges():
                    equal = False
                    break
        return equal

    def testCreateGraph(self):
        # create empty graph
        g = create_graph()
        self.assertEqual(len(g.nodes()), 0)
        # create a simple graph
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        g = create_graph(g=d)
        self.assertEqual(len(g.edges()), 3)
        self.assertEqual(len(g.nodes()), 3)

    def testRest(self):
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        text = ['0:1,2', '1:0,2', '2:0,1']
        g = nx.Graph()
        g.add_nodes_from([x for x in range(0, 3)])
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        self.assertEqual(self.graph_equal(g, convert_to_networkx(d)), True)
        self.assertEqual(d, convert_to_d3(g))
        self.assertEqual(d3_to_text(d), ['0:1,2', '1:0,2', '2:0,1'])
        self.assertEqual(text_to_d3(text), d)

    def testAvailableColor(self):
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        G = convert_to_networkx(d)
        is_available = available_color(G, 0, 0)
        self.assertEqual(is_available, True)
        # color one neighbor
        G.node[1]['node'].color = 0
        is_available = available_color(G, 0, 0)
        self.assertEqual(is_available, False)
        is_available = available_color(G, 0, 1)
        self.assertEqual(is_available, True)
        # color all neighbors
        G.node[2]['node'].color = 1
        is_available = available_color(G, 0, 0)
        self.assertEqual(is_available, False)
        is_available = available_color(G, 0, 1)
        self.assertEqual(is_available, False)
        is_available = available_color(G, 0, 2)
        self.assertEqual(is_available, True)

    def testAvailableColors(self):
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        G = convert_to_networkx(d)
        colors = available_colors(G, 0, 3)
        self.assertEqual(colors, [0, 1, 2])
        # color one neighbor
        G.node[1]['node'].color = 0
        colors = available_colors(G, 0, 3)
        self.assertEqual(colors, [1, 2])
        # color other neighbor
        G.node[2]['node'].color = 1
        colors = available_colors(G, 0, 3)
        self.assertEqual(colors, [2])

    def testValidColoring(self):
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        G = convert_to_networkx(d)
        G.node[0]['node'].color = 0
        G.node[1]['node'].color = 1
        G.node[2]['node'].color = 2
        valid = valid_coloring(G)
        self.assertEqual(valid, True)
        G.node[0]['node'].color = 0
        G.node[1]['node'].color = 0
        G.node[2]['node'].color = 2
        valid = valid_coloring(G)
        self.assertEqual(valid, False)
        G.node[0]['node'].color = 0
        G.node[1]['node'].color = 2
        G.node[2]['node'].color = 2
        valid = valid_coloring(G)
        self.assertEqual(valid, False)
        G.node[0]['node'].color = 2
        G.node[1]['node'].color = 0
        G.node[2]['node'].color = 2
        valid = valid_coloring(G)
        self.assertEqual(valid, False)
        G.node[0]['node'].color = 1
        G.node[1]['node'].color = 1
        G.node[2]['node'].color = 2
        valid = valid_coloring(G)
        self.assertEqual(valid, False)

    def testColorVertex(self):
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        G = convert_to_networkx(d)
        color_vertex(G, 0, 0)
        self.assertEqual(G.node[0]['node'].color, 0)

    def testCopyGraph(self):
        d = {
            "nodes": [0, 1, 2],
            "edges": [
                [0, 1],
                [0, 2],
                [1, 2]
            ]
        }
        G = convert_to_networkx(d)
        H = copy_graph(G)
        # change H color and should not affect G
        H.node[0]['node'].color = 0
        self.assertNotEqual(G.node[0]['node'].color, 0)
        H.node[1]['node'].color = 1
        self.assertNotEqual(G.node[1]['node'].color, 1)
