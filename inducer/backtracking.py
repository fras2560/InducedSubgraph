'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-02
@note: backtrack coloring_aux method
'''
import logging
import networkx as nx
from inducer.graph import color_vertex,\
    copy_graph_colors,\
    available_colors,\
    get_color,\
    valid_coloring,\
    copy_graph,\
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
        g_size = len(list(G.neighbors(node)))
        constraining = g_size - len(list(already_colored))
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
