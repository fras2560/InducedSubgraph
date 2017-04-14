'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-02
@note: backtrack coloring_aux method
'''
import unittest
import logging
import networkx as nx
from inducer.graph import color_vertex,\
                          copy_graph_colors,\
                          available_colors,\
                          get_color,\
                          valid_coloring,\
                          copy_graph,\
                          convert_to_networkx,\
                          chromatic_number
COUNT = 0
ALL_OPTIONS = {"forward_check": lambda x, y: forward_check(x, y),
               "get_colors": lambda x, y, z:
               least_constraining_colors(x, y, z),
               "next_node": lambda x, y: ordering_node(x, y)}


class MaxStepsException(Exception):
    """A class that is raised when maximum numbers of steps are reached
    """
    pass


def forward_check(G, chromatic):
    """Returns True if forward check holds

    Parameters:
        G: the networkx graph
        chromatic: the number of colors used
    Returns:
        forward: True if forward check is valid, False otherwise (boolean)
    """
    forward = True
    for node in G.nodes():
        if(get_color(G, node) is None and
           len(available_colors(G, node, chromatic)) == 0):
            forward = False
            break
    return forward


def inducer_coloring(G):
    (H, chromatic) = coloring(G)
    colors = [[] for __ in range(0, chromatic)]
    for node in H.nodes():
        colors[get_color(H, node)].append(node)
    return colors


def least_constraining_colors(G, vertex, chromatic):
    """Returns a list of available colors order by level of constraint

    Parameters:
        G: the networkx graph
        vertex: the vertex to be used (int)
        chromatic: the number of colors to use (int)
    Returns:
        colors the list of colors sorted be level of constraint
    """
    # what colors are available to vertex
    neighbors_colors = [get_color(G, neighbor)
                        for neighbor in G.neighbors(vertex)
                        if get_color(G, neighbor) is not None]
    colors = [x for x in range(0, chromatic) if x not in neighbors_colors]
    # get all the possible options of colors available to neighbors
    neighbor_options = [available_colors(G, neighbor, chromatic)
                        for neighbor in G.neighbors(vertex)
                        if get_color(G, neighbor) is None]
    # now flatten the list of lists to a single list
    neighbor_options = [item for sublist in neighbor_options
                        for item in sublist]
    # count how many times it appears
    count = []
    for color in colors:
        count.append((color, neighbor_options.count(color)))
    # sort by the lower first
    count.sort(key=lambda x: x[1])
    colors = [x[0] for x in count]
    return colors


def ordering_node(G, chromatic):
    """Returns most constraining vertex with most constrained as tiebreaker

    Parameters:
        G: the networkx graph
        chromatic: the number of colors to use
    Returns:
        vertex: the index of the vertex to use next
    """
    colors = [x for x in range(0, chromatic)]
    vertex = None
    best_constraining = None
    best_constrained = None
    constraining = None
    constrained = None
    nodes = [x for x in G.nodes() if get_color(G, x) is None]
    for node in nodes:
        colors = [x for x in range(0, chromatic)]
        already_colored = [get_color(G, x) for x in G.neighbors(node)
                           if get_color(G, x) is not None]
        constraining = len(G.neighbors(node)) - len(already_colored)
        if vertex is None or constraining >= best_constraining:
            constrained = len([c for c in colors if c not in already_colored])
            if constraining == best_constraining:
                # need to check tie
                if constrained >= best_constrained:
                    # do not switch to the other node
                    node = vertex
                    constrained = best_constrained
            best_constraining = constraining
            best_constrained = constrained
            vertex = node
    return vertex


def always_forward(G, chromatic):
    """Returns True since always a path forward"""
    return True


def get_first_node(G, chromatic):
    """Returns the first node not colored"""
    node = None
    for vertex in G.nodes():
        if get_color(G, vertex) is None:
            node = vertex
            break
    return node


def coloring(G, logger=None):
    """Returns a coloring and chromatic number"""
    options = {"forward_check": forward_check,
               "get_colors": least_constraining_colors,
               "next_node": ordering_node}
    (H, __) = coloring_aux(G, options, logger=logger)
    return (H, chromatic_number(H))


def coloring_aux(G, options, logger=None):
    """Returns a coloring_aux of G and number of steps

    Parameters:
        G: the networkx graph
        options: a dictionary of options for forward checking,
                 ordering(mcv & lcv) and approx to chromatic number
        logger: the logger to use
    Returns
        (color, steps): a colored networkx graph and # of steps
    """
    if logger is None:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
    if 'approx' in options.keys():
        chromatic = options['approx'](G)
    else:
        # default is to use clique width
        chromatic = nx.graph_clique_number(G)
    if 'forward_check' in options.keys():
        forward = options['forward_check']
    else:
        # default is no forward checking
        forward = always_forward
    if 'next_node' in options.keys():
        next_node = options['next_node']
    else:
        # default is to get first available node
        next_node = get_first_node
    if 'get_colors' in options.keys():
        get_colors = options['get_colors']
    else:
        # default is a function that gets
        # all available colors not shared by neighbors
        get_colors = available_colors
    color = backtrack(copy_graph(G),
                      chromatic,
                      forward,
                      next_node,
                      get_colors,
                      logger)
    while color is None:
        chromatic += 1
        color = backtrack(copy_graph(G),
                          chromatic,
                          forward,
                          next_node,
                          get_colors,
                          logger)
    global COUNT
    steps = COUNT
    COUNT = 0
    return (color, steps)


def backtrack(G, chromatic, forward_check, get_vertex, get_colors, logger):
    """Returns a coloring_aux of G with chromatic number of colors

    Parameters:
        G: the networkx graph
        chromatic: the chromatic number currently checking
        forward_check: the function to check forward
        get_vertex: get the next vertex
        get_colors: get the colors available to the vertex
        logger: the logger to be used
    Returns:
        solution: the colored graph
    """
    # COUNT is the number assignments, since an assignment auto call backtrack
    global COUNT
    COUNT += 1
    # get the next variable to work with
    vertex = get_vertex(G, chromatic)
    solution = None
    if vertex is not None:
        # if heuristic then will get the least constraining value
        colors = get_colors(G, vertex, chromatic)
        if len(colors) > 0:
            # move to next variable
            for color in colors:
                # we got a guess of the square
                color_vertex(G, vertex, color)
                # check if there is a path forward
                proceed = forward_check(G, chromatic)
                # move onto the next variable
                if proceed:
                    solution = backtrack(copy_graph_colors(G),
                                         chromatic,
                                         forward_check,
                                         get_vertex,
                                         get_colors,
                                         logger)
                    # check if out guess was right
                    if valid_coloring(solution):
                        # done
                        logger.debug("Correct solution was found")
                        break
                else:
                    pass
        else:
            # no solution
            solution = None
    else:
        # must have a proposed solution
        solution = G
    return solution


class testBacktracking(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBacktrackBasics(self):
        # test C5
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
        (colored_G, steps) = coloring_aux(G, {})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 15)

    def testBacktrackForwardCheck(self):
        # test C5
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
        forward = forward_check
        (colored_G, steps) = coloring_aux(G, {'forward_check': forward})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 13)

    def testBacktrackOrdering(self):
        # test C5
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
        next_node = ordering_node
        (colored_G, steps) = coloring_aux(G, {'next_node': next_node})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 17)

    def testBacktrackLeastConstrainingColors(self):
        # test C5
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
        lcc = least_constraining_colors
        (colored_G, steps) = coloring_aux(G, {'get_colors': lcc})
        self.assertEqual(valid_coloring(colored_G), True)
        self.assertEqual(chromatic_number(colored_G), 3)
        self.assertEqual(steps, 15)

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

    def testLeastConstrainingColors(self):
        # test C5
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
        color_vertex(G, 4, 0)
        color_vertex(G, 3, 1)
        colors = least_constraining_colors(G, 1, 3)
        self.assertEqual([0, 1, 2], colors)
        color_vertex(G, 4, 0)
        color_vertex(G, 3, 1)
        color_vertex(G, 2, 0)
        colors = least_constraining_colors(G, 1, 3)
        self.assertEqual([1, 2], colors)
        # test a diamond
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
        color_vertex(G, 0, 0)
        color_vertex(G, 2, 1)
        colors = least_constraining_colors(G, 3, 3)
        self.assertEqual([0, 2], colors)

    def testForwardCheck(self):
        # test C5
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
        # there is a path forward
        forward = forward_check(G, 2)
        self.assertEqual(forward, True)
        # color both neighbors of 1 so no path forward
        color_vertex(G, 0, 0)
        color_vertex(G, 2, 1)
        forward = forward_check(G, 2)
        self.assertEqual(forward, False)
        # now expand number of colors opening up path forward
        forward = forward_check(G, 3)
        self.assertEqual(forward, True)

    def testOrderingNodeC5(self):
        # test C5
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
        node = ordering_node(G, 2)
        self.assertEqual(node, 0)
        # color vertex 0
        color_vertex(G, 0, 0)
        node = ordering_node(G, 2)
        self.assertEqual(node, 2)
        # color vertex 2
        color_vertex(G, 2, 1)
        node = ordering_node(G, 2)
        self.assertEqual(node, 3)
        # color vertex 3
        color_vertex(G, 3, 0)
        node = ordering_node(G, 2)
        self.assertEqual(node, 1)
        # color vertex 1
        color_vertex(G, 1, 2)
        node = ordering_node(G, 3)
        self.assertEqual(node, 4)
        # color vertex =4
        color_vertex(G, 4, 1)
        node = ordering_node(G, 3)
        self.assertEqual(node, None)

    def testOrderingNodeTiebreaker(self):
        # test the tiebreaker
        d = {
                "nodes": [0, 1, 2, 3, 4, 5, 6],
                "edges": [
                          [0, 2],
                          [0, 3],
                          [0, 4],
                          [1, 4],
                          [1, 5],
                          [1, 6],
                          [3, 4],
                          [4, 5],
                         ]
             }
        G = convert_to_networkx(d)
        # both have the same amount of moves (so first one aka 0)
        color_vertex(G, 4, 0)
        color_vertex(G, 2, 1)
        color_vertex(G, 6, 1)
        node = ordering_node(G, 2)
        self.assertEqual(node, 0)
        # 0 has less moves
        color_vertex(G, 4, 0)
        color_vertex(G, 2, 1)
        color_vertex(G, 6, 0)
        node = ordering_node(G, 2)
        self.assertEqual(node, 0)
        # 1 has less moves
        color_vertex(G, 4, 0)
        color_vertex(G, 2, 0)
        color_vertex(G, 6, 1)
        node = ordering_node(G, 2)
        self.assertEqual(node, 1)

    def testBacktrackingColorSubOptimal(self):
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
        self.assertEqual(chromatic, 3)
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
        self.assertEqual(chromatic, 4)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
