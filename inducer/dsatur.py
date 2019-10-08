'''
@author: Dallas Fraser
@id: 20652186
@class: CS686
@date: 2016-04-05
@note: coloring_aux with a greedy algorithm
'''
import logging
from inducer.graph import available_color,\
    color_vertex,\
    copy_graph,\
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
