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
    hub = 0 # 0-vertex is the hub of claw
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
    for vertex in range(0,n):
        # add all the vertices
        cycle.add_node(vertex)
    for vertex in range(0,n):
        # add all the edges
        cycle.add_edge(vertex, (vertex+1) % n)
        cycle.add_edge(vertex, (vertex-1) % n)
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
    wheel = make_cycle(n-1)
    wheel.add_node(n-1)
    for edge in range(0,n-1):
        wheel.add_edge(edge,n-1)
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
            F.add_edge(v1,v2+shift)
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
    graph = {'nodes': [], 'edges':[]}
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
    graph = {'nodes':[], 'edges':[]}
    for line in lines:
        entries = line.split(":")
        node = int(entries[0])
        entries[1] = entries[1].replace(" ", "")
        edges = entries[1].split(",")
        for edge in edges:
            if edge != '':
                e = int(edge)
                if [e, node] not in graph['edges'] and node != e:
                    # do not want to add an edges twice
                    graph['edges'].append([node, e])
        graph['nodes'].append(node)
#     except:
#         graph = None
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
        line = str(node) +":"
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

import unittest
import os
class tester(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    def testMakeDiamond(self):
        g = make_diamond()
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, g.edges(), "Make Diamond: failed on edges")
        self.assertEqual(vertices, g.nodes(),
                         "Make Diamond: failed on vertices")
    def testMakeCoDiamond(self):
        g = make_co_diamond()
        edges = [(2, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, g.edges(),
                         "Make Co-Diamond: failed on edges")
        self.assertEqual(vertices, g.nodes(),
                         "Make Co-Diamond: failed on vertices")
    def testMakeClaw(self):
        g = make_claw()
        edges = [(0, 1), (0, 2), (0, 3)]
        vertices =[0, 1, 2, 3]
        self.assertEqual(edges, g.edges(), "Make Claw: failed on edges")
        self.assertEqual(vertices, g.nodes(), "Make Claw: failed on vertices")

    def testMakeCoClaw(self):
        g = make_co_claw()
        edges = [(1, 2), (1, 3), (2, 3)]
        vertices =[0, 1, 2, 3]
        self.assertEqual(edges, g.edges(), "Make Co-Claw: failed on edges")
        self.assertEqual(vertices, g.nodes(),
                         "Make Co-Claw: failed on vertices")

    def testMakeCycle(self):
        g = make_cycle(3)
        edges = [(0,1), (0,2), (1,2)]
        vertices = [0, 1, 2]
        self.assertEqual(edges, g.edges(), "Make Cycle: failed on edges")
        self.assertEqual(vertices, g.nodes(), "Make Cycle: failed on vertices")

    def testJoin(self):
        # wheel test
        g = make_cycle(5)
        h = nx.Graph()
        h.add_node(0)
        f = join(g, h)
        expect = nx.wheel_graph(6) # expect a wheel
        self.assertEqual(expect.nodes(), f.nodes(),
                         " Join: nodes failed on wheel test")
        self.assertEqual(nx.is_isomorphic(f, expect), True,
                         " Join: edges failed on wheel test")
        # join of two trianges = K6
        g = nx.complete_graph(3)
        h = nx.complete_graph(3)
        f = join(g, h)
        expect = nx.complete_graph(6)
        self.assertEqual(expect.nodes(), f.nodes(), 
                         "Join: nodes failed for K6 test")
        self.assertEqual(nx.is_isomorphic(f, expect), True,
                         " Join: edges failed on wheel K6 test")

    def testWheel(self):
        # w5
        w = make_wheel(5)
        g = make_cycle(4)
        g.add_node(5)
        g.add_edge(0,4)
        g.add_edge(1,4)
        g.add_edge(2,4)
        g.add_edge(3,4)
        self.assertEqual(w.edges(), g.edges(), "Make wheel: Failed for W5 test")

    def testConvertToNetworkx(self):
        g = {'edges': [[1,2]], 'nodes':[0, 1, 2]}
        result = convert_to_networkx(g)
        self.assertEqual(result.edges(), [(1, 2)],
                         "Convert to Networkx: Failed to add edges")
        self.assertEqual(result.nodes(), [0, 1, 2],
                         "Convert to Networkx: Failed to add nodes")

    def testConverToD3(self):
        g = make_cycle(4)
        result = convert_to_d3(g)
        edges = [(0,1), (0,3), (1,2), (2,3)]
        nodes = [0, 1, 2 ,3] 
        self.assertEqual(result['edges'], edges,
                         "Convert to D3: failed to add edges")
        self.assertEqual(result['nodes'], nodes,
                         "Convert to D3: failed to add nodes")

    def testTextToD3(self):
        directory = os.getcwd()
        while "inducer" in directory:
            directory = os.path.dirname(directory)
        claw = {'edges':[[0, 1], [0, 2], [0, 3]], 'nodes':[0, 1, 2, 3]}
        c7 = {'edges':[[0, 1], [0, 6], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]] ,
              'nodes':[0, 1, 2, 3, 4, 5, 6]}
        co_claw = {'edges':[[1, 2], [1, 3], [2, 3]], 'nodes':[0, 1, 2, 3] }
        tests = {'test1.txt': claw, 'test2.txt': c7, 'test3.txt': co_claw}
        for file, expect in tests.items():
            filepath = os.path.join(directory, "graphs", file)
            with open(filepath) as f:
                content = f.read()
                lines = content.replace("\r", "")
                lines = lines.split("\n")
                result = text_to_d3(lines)
                self.assertEqual(expect ,result ,
                                 "Test to D3 Failed: %s" % file)


