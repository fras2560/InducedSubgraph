"""
-------------------------------------------------------
helper
a couple of helper functions
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-10
-------------------------------------------------------
"""
import networkx as nx
import unittest


def make_co_R():
    '''
    a method to assemble a co-R graph
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_diamond()
    g.add_node(4)
    g.add_node(5)
    g.add_edge(0, 4)
    g.add_edge(1, 4)
    g.add_edge(2, 4)
    g.add_edge(3, 5)
    return g


def make_bridge():
    '''
    a method to assemble a bridge graph
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_co_R()
    g.add_edge(0, 5)
    g.add_edge(1, 5)
    return g


def make_clique(n):
    '''
    makes a clique of size n
    Parameters:
        n: the size of the clique (int)
    Returns:
        clique: the graph (networkx)
    '''
    clique = nx.Graph()
    for v in range(0, n):
        clique.add_node(v)
    end = len(clique.nodes())
    for target in clique.nodes():
        for source in range(target + 1, end):
            clique.add_edge(target, source)
    return clique


def make_kite():
    '''
    make_kite
    assembles a kite (co-chair)
    Parameters:
        None
    Returns:
        kite: the kite (Graph)
    '''
    kite = make_diamond()
    kite.add_node(4)
    kite.add_edge(2, 4)
    return kite


def make_claw():
    '''
    make_claw
    assembles a claw
    Parameters:
        None
    Returns:
        claw: the claw (networkx)
    '''
    claw = nx.Graph()
    for x in range(0, 4):
        # add four vertices
        claw.add_node(x)
    # 0-vertex is the hub of claw
    hub = 0
    for x in range(1, 4):
        claw.add_edge(hub, x)
    return claw


def make_diamond():
    '''
    make_diamond
    assembles a diamond
    Parameters:
        None
    Returns:
        diamond: the diamond graph (networkx)
    '''
    diamond = nx.Graph()
    for x in range(0, 4):
        # add four vertices
        diamond.add_node(x)
    diamond.add_edge(0, 1)
    diamond.add_edge(0, 2)
    diamond.add_edge(0, 3)
    diamond.add_edge(1, 2)
    diamond.add_edge(1, 3)
    return diamond


def make_co_diamond():
    '''
    make_co_diamond
    assembles a co-diamond
    Parameters:
        None
    Returns:
        co_diamond: the co-diamond graph (networkx)
    '''
    return nx.complement(make_diamond())


def make_co_claw():
    '''
    make_co_claw
    assembles a co-claw
    Parameters:
        None
    Returns:
        co_claw: the co_claw (networkx)
    '''
    return nx.complement(make_claw())


def make_cycle(n):
    '''
    make_cycle
    assembles a cycle with n vertices
    Parameters:
        n: the number of vertices in cycle (int)
    Returns:
        cycle: the cycle (networkx)
    '''
    cycle = nx.Graph()
    for vertex in range(0, n):
        # add all the vertices
        cycle.add_node(vertex)
    for vertex in range(0, n):
        # add all the edges
        cycle.add_edge(vertex, (vertex + 1) % n)
        cycle.add_edge(vertex, (vertex - 1) % n)
    return cycle


def make_wheel(n):
    '''
    make_wheel
    assembles a wheel with n vertices
    Parameters:
        n: the number of vertices in the wheel (int)
    Returns:
        wheel: the wheel (networkx)
    '''
    wheel = make_cycle(n - 1)
    wheel.add_node(n - 1)
    for edge in range(0, n - 1):
        wheel.add_edge(edge, n - 1)
    return wheel


def join(G, H):
    '''
    join
    a function which (complete) joins one graph G to graph H
    Parameters:
        G: Graph with at least one vertice (networkx)
        H: Graph with at least one vertice (networkx)
    Returns:
        F: The join of G and H (Graph)
    '''
    # add all of
    F = nx.Graph()
    F.add_nodes_from(G.nodes())
    F.add_edges_from(G.edges())
    shift = G.number_of_nodes()
    # add all nodes of H
    for vertex in H.nodes():
        F.add_node(vertex)
    # add all of F edges
    for e1, e2 in H.edges():
        F.add_edge(e1 + shift, e2 + shift)
    # join the two sets of nodes
    for v1 in G.nodes():
        for v2 in H.nodes():
            F.add_edge(v1, v2 + shift)
    return F


def convert_to_networkx(g):
    '''
    convert_to_networkx
    a function which take a {'nodes':[n1],'edges':[[n1,n2]]}
    and converts it to a networkx Graph object
    Parameters:
        g: the python dictionary repesentation of a graph (dictionary)
    Returns:
        graph: the graph G (networkx)
    '''
    graph = nx.Graph()
    for node in g['nodes']:
        graph.add_node(node)
    for edge in g['edges']:
        graph.add_edge(edge[0], edge[1])
    return graph


def convert_to_d3(g):
    '''
    conver_to_d3
    a function which takes a networkx Graph object and converts it to
    a {'nodes':[n1],'edges':[[n1,n2]]}
    Parameters:
        g: the graph G (networkx)
    Returns:
        graph: python dictionary representation of a graph (dictionary)
    '''
    graph = {'nodes': [], 'edges': []}
    for node in g.nodes():
        graph['nodes'].append(node)
    for edge in g.edges():
        graph['edges'].append(edge)
    return graph


def text_to_d3(lines):
    '''
    text_to_networkx
    a function that takes the lines from a text file and puts into a format for
    d3 graph
    Parameters:
        lines: a list of lines from the text file (list)
    Returns:
        d3: a d3 representation of the graph
    '''
#     try:
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
    '''
    d3_to_text
    a function that takes a d3 representation and converts it to text
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


def complement(g):
    '''
    complement
    a function which takes the complement of g
    Parameters:
        g: the graph (networkx)
    Returns:
        co_g: the complement graph (networkx)
    Note:
        does not have a unittest since not needed (written by someone else)
    '''
    return nx.complement(g)


def make_co_twin_c5():
    '''
    a function to assemble a co-Twin-C5
    Parameters:
        None
    Returns:
        g: the graph g (networkx)
    '''
    g = make_cycle(5)
    g.add_node(5)
    g.add_edge(5, 0)
    g.add_edge(5, 2)
    g.add_edge(5, 1)
    return g


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
