'''
@author: Dallas Fraser
@date: 2019-08-10
@summary: Holds a function to check if a given graph is critical
'''
from inducer.dcolor import dense_color_wrapper
from inducer.colorable import coloring as color


def critical(G, logger=None, dense=False):
    '''
    a method that finds if the graph is critical
    Parameters:
        G: the graph to check (networkx)
        logger: an optional logger
        dense: True if the graph is quite dense (boolean)
    Returns:
        K: how many colors the graphs need to be colored (int),
            None if the graph is not critical
    '''
    if dense:
        coloring = color
    else:
        coloring = dense_color_wrapper
    is_critical = True
    nodes = list(G.nodes())
    index = 0
    chromatic = len(coloring(G))
    while is_critical and index < len(nodes):
        g = G.copy()
        g.remove_node(nodes[index])
        check = len(coloring(g))
        if check != (chromatic - 1):
            if logger is not None:
                logger.info(index)
                logger.info("G is not critical")
            is_critical = False
        index += 1
    K = None
    if is_critical:
        K = chromatic
    return K
