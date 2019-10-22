'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-02
@note: contains functions for creating networkx graphs with GraphNodes
'''
from os.path import isfile
from inducer.graph.graph_node import GraphNode
import networkx as nx


def is_colored(G, vertex):
    """Returns whether the vertex is colored or not"""
    return G.nodes[vertex]['node'].color is not None


def chromatic_number(G):
    """Returns the chromatic number of G

    Parameters:
        G: the networkx graph
    Returns:
        : the chromatic number of G (int)
    """
    colors = []
    for node in G:
        if G.nodes[node]['node'].color not in colors:
            colors.append(G.nodes[node]['node'].color)
    return len(colors)


def copy_graph_colors(G):
    """Returns a copy of the G while maintaining its colors
    """
    H = nx.Graph()
    for n in G.nodes():
        node = GraphNode(index=n,
                         logger=G.nodes[n]['node'].logger,
                         color=G.nodes[n]['node'].color,
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
    G.nodes[vertex]['node'].color = color


def get_color(G, vertex):
    return G.nodes[vertex]['node'].color


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
                if (G.nodes[neighbor]['node'].color ==
                        G.nodes[node]['node'].color):
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
        if G.nodes[neighbor]['node'].color == color:
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
            index = colors.index(G.nodes[neighbor]['node'].color)
            colors.pop(index)
        except Exception:
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
        except Exception:
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
