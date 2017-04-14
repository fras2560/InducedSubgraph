'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-02
@note: contains functions for creating networkx graphs with GraphNodes
'''
import networkx as nx
from os.path import isfile
from inducer.graph.graph_node import GraphNode
import unittest
import copy


def is_colored(G, vertex):
    """Returns whether the vertex is colored or not"""
    return G.node[vertex]['node'].color is not None


def chromatic_number(G):
    """Returns the chromatic number of G

    Parameters:
        G: the networkx graph
    Returns:
        : the chromatic number of G (int)
    """
    colors = []
    for node in G:
        if G.node[node]['node'].color not in colors:
            colors.append(G.node[node]['node'].color)
    return len(colors)


def copy_graph_colors(G):
    """Returns a copy of the G while maintaining its colors
    """
    H = nx.Graph()
    for n in G.nodes():
        node = GraphNode(index=n,
                         logger=G.node[n]['node'].logger,
                         color=G.node[n]['node'].color,
                         )
        H.add_node(n, node=node)
    for edge in G.edges():
        H.add_edge(edge[0], edge[1])
    return H


def copy_graph(G):
    """Returns a copy of the G
    """
    return convert_to_networkx(convert_to_d3(G))


def color_vertex(G, vertex, color):
    """Colors a vertex of G

    Parameters:
        G: a networkx graph with Graph Nodes
        vertex: the vertex number (int)
        color: the color
    """
    G.node[vertex]['node'].color = color


def get_color(G, vertex):
    return G.node[vertex]['node'].color


def valid_coloring(G):
    """Returns True if G's coloring is valid

    Parameters:
        G: a networkx graph with Graph Nodes
    Return:
        valid: True if valid coloring (boolean)
    """
    valid = False
    if G is not None:
        valid = True
        for node in G.nodes():
            for neighbor in G.neighbors(node):
                if (G.node[neighbor]['node'].color ==
                        G.node[node]['node'].color):
                    valid = False
                    break
            if not valid:
                break
    return valid


def available_color(G, vertex, color):
    """Returns True if color is available or not

    Parameters:
        G: a networkx graph with Graph Nodes
        vertex: the vertex number (int)
        color: the color to see if available
    Returns:
        available: True if color is available (boolean)
    """
    available = True
    for neighbor in G.neighbors(vertex):
        if G.node[neighbor]['node'].color == color:
            available = False
            break
    return available


def available_colors(G, vertex, number_of_colors):
    """Returns all the available colors for vertex

    Parameters:
        G: a networkx graph with Graph Nodes
        vertex: the vertex number (int)
        number_of_colors: the number of colors (int)
    Returns:
        colors: list of available colors (list)
    """
    colors = [x for x in range(0, number_of_colors)]
    for neighbor in G.neighbors(vertex):
        try:
            index = colors.index(G.node[neighbor]['node'].color)
            colors.pop(index)
        except:
            pass
    return colors


def create_graph(g=None, text_file=None, logger=None):
    """Returns a networkx Graph with GraphNodes

    Parameters:
        g: the dictionary representation of a graph (dictionary)
        text_file: the file path to a text file with the graph (file)
        logger: the logger the graph should use (logger)
    Returns:
        graph: the networkx graph
    """
    if g is not None and text_file is not None:
        raise Exception("Only g or text_file should be given")
    graph = nx.Graph()
    if g is not None:
        graph = convert_to_networkx(g, logger=logger)
    if text_file is not None:
        with open(text_file) as f:
            if not isfile(text_file):
                raise Exception("File not found")
            lines = []
            for line in f:
                lines.append(line)
            graph = convert_to_networkx(text_to_d3(lines))
    return graph


def convert_to_networkx(g, logger=None):
    ''' Returns a networkx graph

    Parameters:
        g: the python dictionary repesentation of a graph (dictionary)
    Returns:
        graph: the graph G (networkx)
    '''
    graph = nx.Graph()
    for node in g['nodes']:
        graph.add_node(node, node=GraphNode(index=node, logger=logger))
    for edge in g['edges']:
        graph.add_edge(edge[0], edge[1])
    return graph


def convert_to_d3(g):
    '''Returns a dictionary representation of a graph used for d3

    Parameters:
        g: the graph G (networkx)
    Returns:
        graph: python dictionary representation of a graph (dictionary)
                eg. {'nodes':[n1],'edges':[[n1,n2]]}
    '''
    graph = {'nodes': [], 'edges': []}
    for node in g.nodes():
        graph['nodes'].append(node)
    for edge in g.edges():
        graph['edges'].append(list(edge))
    return graph


def text_to_d3(lines):
    ''' Returns a dictionary representation of a graph used for d3

    Parameters:
        lines: a list of lines from the text file (list)
    Returns:
        d3: a d3 representation of the graph
    '''
    graph = {'nodes': [], 'edges': []}
    for line in lines:
        entries = line.split(":")
        try:
            node = int(entries[0])
        except:
            node = None
        if (len(entries) > 1):
            entries[1] = entries[1].replace(" ", "")
            edges = entries[1].split(",")
            for edge in edges:
                if edge != '':
                    e = int(edge)
                    if [e, node] not in graph['edges'] and node != e:
                        # do not want to add an edges twice
                        graph['edges'].append([node, e])
        if node is not None:
            graph['nodes'].append(node)
    return graph


def d3_to_text(g):
    '''Returns a text string of a graph g (used for saving to files)

    Parameters:
        g: the d3 graph representation
    Returns:
        graph: list of text representation the graph (list)
    '''
    graph = []
    for node in g['nodes']:
        line = str(node) + ":"
        edges = []
        for edge in g['edges']:
            if node == edge[0]:
                edges.append(str(edge[1]))
            elif node == edge[1]:
                edges.append(str(edge[0]))
        line = line + ",".join(edges)
        graph.append(line)
    return graph


class testFunctions(unittest.TestCase):
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
                "edges":  [
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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
