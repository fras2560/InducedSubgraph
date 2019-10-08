'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Tests for helper functions
'''
from inducer.helper import make_claw, make_cycle, join, make_diamond,\
    make_wheel, make_co_diamond, make_co_claw, convert_to_d3,\
    convert_to_networkx, text_to_d3
import networkx as nx
import os
import unittest


class tester(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMakeDiamond(self):
        g = make_diamond()
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, list(g.edges()),
                         "Make Diamond: failed on edges")
        self.assertEqual(vertices, list(g.nodes()),
                         "Make Diamond: failed on vertices")

    def testMakeCoDiamond(self):
        g = make_co_diamond()
        edges = [(2, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, list(g.edges()),
                         "Make Co-Diamond: failed on edges")
        self.assertEqual(vertices, list(g.nodes()),
                         "Make Co-Diamond: failed on vertices")

    def testMakeClaw(self):
        g = make_claw()
        edges = [(0, 1), (0, 2), (0, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, list(g.edges()), "Make Claw: failed on edges")
        self.assertEqual(vertices, list(g.nodes()),
                         "Make Claw: failed on vertices")

    def testMakeCoClaw(self):
        g = make_co_claw()
        edges = [(1, 2), (1, 3), (2, 3)]
        vertices = [0, 1, 2, 3]
        self.assertEqual(edges, list(g.edges()),
                         "Make Co-Claw: failed on edges")
        self.assertEqual(vertices, list(g.nodes()),
                         "Make Co-Claw: failed on vertices")

    def testMakeCycle(self):
        g = make_cycle(3)
        edges = [(0, 1), (0, 2), (1, 2)]
        vertices = [0, 1, 2]
        self.assertEqual(edges, list(g.edges()),
                         "Make Cycle: failed on edges")
        self.assertEqual(vertices, list(g.nodes()),
                         "Make Cycle: failed on vertices")

    def testJoin(self):
        # wheel test
        g = make_cycle(5)
        h = nx.Graph()
        h.add_node(0)
        f = join(g, h)
        # expect a wheel
        expect = nx.wheel_graph(6)
        self.assertEqual(expect.nodes(), f.nodes(),
                         " Join: nodes failed on wheel test")
        self.assertEqual(nx.is_isomorphic(f, expect), True,
                         " Join: edges failed on wheel test")
        # join of two trianges = K6
        g = nx.complete_graph(3)
        h = nx.complete_graph(3)
        f = join(g, h)
        expect = nx.complete_graph(6)
        self.assertEqual(expect.nodes(),
                         f.nodes(),
                         "Join: nodes failed for K6 test")
        self.assertEqual(nx.is_isomorphic(f, expect),
                         True,
                         " Join: edges failed on wheel K6 test")

    def testWheel(self):
        # w5
        w = make_wheel(5)
        g = make_cycle(4)
        g.add_node(5)
        g.add_edge(0, 4)
        g.add_edge(1, 4)
        g.add_edge(2, 4)
        g.add_edge(3, 4)
        self.assertEqual(w.edges(),
                         g.edges(),
                         "Make wheel: Failed for W5 test")

    def testConvertToNetworkx(self):
        g = {'edges': [[1, 2]], 'nodes': [0, 1, 2]}
        result = convert_to_networkx(g)
        self.assertEqual(list(result.edges()), [(1, 2)],
                         "Convert to Networkx: Failed to add edges")
        self.assertEqual(list(result.nodes()), [0, 1, 2],
                         "Convert to Networkx: Failed to add nodes")

    def testConverToD3(self):
        g = make_cycle(4)
        result = convert_to_d3(g)
        edges = [(0, 1), (0, 3), (1, 2), (2, 3)]
        nodes = [0, 1, 2, 3]
        self.assertEqual(result['edges'], edges,
                         "Convert to D3: failed to add edges")
        self.assertEqual(result['nodes'], nodes,
                         "Convert to D3: failed to add nodes")

    def testTextToD3(self):
        directory = os.getcwd()
        while "inducer" in directory:
            directory = os.path.dirname(directory)
        claw = {'edges': [[0, 1], [0, 2], [0, 3]], 'nodes': [0, 1, 2, 3]}
        c7 = {'edges': [[0, 1],
                        [0, 6],
                        [1, 2],
                        [2, 3],
                        [3, 4],
                        [4, 5],
                        [5, 6]],
              'nodes': [0, 1, 2, 3, 4, 5, 6]}
        co_claw = {'edges': [[1, 2], [1, 3], [2, 3]], 'nodes': [0, 1, 2, 3]}
        tests = {'test1.txt': claw, 'test2.txt': c7, 'test3.txt': co_claw}
        for f, expect in tests.items():
            filepath = os.path.join(directory, "graphs", f)
            with open(filepath) as f:
                content = f.read()
                lines = content.replace("\r", "")
                lines = lines.split("\n")
                result = text_to_d3(lines)
                self.assertEqual(expect,
                                 result,
                                 "Test to D3 Failed: %s" % f)
