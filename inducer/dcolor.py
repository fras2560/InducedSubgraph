"""
-------------------------------------------------------
dcolor
a module to determine the chromatic number of a graph
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
from itertools import permutations
from pprint import PrettyPrinter
import logging
import copy
import networkx as nx


def dense_color_wrapper(G, logger=None):
    return Dcolor(G, logger=logger).color()


class Dcolor():

    def __init__(self, graph, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.coloring = None
        self.graph = graph
        self.pp = PrettyPrinter(indent=4)

    def chromaic_number(self):
        '''
        a method to determine the chromatic number of the graph
        Parameters:
            None
        Returns:
            : the chromatic number (int)
        '''
        if self.coloring is None:
            self.color()
        return len(self.coloring)

    def color(self):
        '''
        a method to determine a graph coloring
        Parameters:
            None
        Returns:
            self.coloring: the graph coloring (list)
        '''
        if self.coloring is None:
            self.color_aux()
        return self.coloring

    def create_clique_list(self):
        '''
        a method to create a list of cliques
        Parameters:
            None
        Returns:
            cliques: the list of cliques (list)
            chromatic: the chromatic number (int)
            l_index: the largest clique index (int)
        '''
        g = self.graph.copy()
        chromatic = 0
        l_index = 0
        index = 0
        cliques = []
        while len(g.nodes()) > 0:
            largest = 0
            for clique in nx.find_cliques(g):
                if len(clique) > largest:
                    largest = len(clique)
                    largest_clique = clique
            clique = []
            for node in largest_clique:
                g.remove_node(node)
                clique.append([node])
            if len(clique) > chromatic:
                chromatic = len(clique)
                largest = clique
                l_index = index
            cliques.append(clique)
            index += 1
        return cliques, chromatic, l_index

    def color_aux(self):
        '''
        a method to help with coloring
        Sets self.coloring to a valid coloring
        Parameters:
            None
        Returns:
            None
        '''
        self.logger.debug("Coloring")
        cliques, chromatic, index = self.create_clique_list()
        done = False
        if chromatic == len(self.graph.nodes()):
            done = True
            coloring = cliques[0]
            self.logger.debug("Graph is a Clique: %d" % chromatic)
        elif chromatic == 2:
            cycles = nx.cycle_basis(self.graph)
            odd = False
            for cycle in cycles:
                if len(cycle) % 2 == 1:
                    odd = True
            if odd:
                largest = cliques.pop(index)
                largest.append([])
                chromatic += 1
            else:
                largest = cliques.pop(index)
        else:
            largest = cliques.pop(index)
        while not done:
            self.logger.info('Testing Chromatic Number: %d' % chromatic)
            coloring = self.coloring_step(cliques, largest)
            if coloring is None:
                largest.append([])  # equivalent to adding a new color
                chromatic += 1
            else:
                done = True
        self.coloring = coloring

    def coloring_step(self, cliques, coloring):
        '''
        a recursive function that acts as one step in the coloring
        Parameters:
            cliques: a list of the cliques (list)
            coloring: an initial coloring (list)
        Returns:
            coloring: None if no coloring is possible
        '''

        if len(cliques) == 0:
            result = coloring
        else:
            added = False
            valid = []
            for pc in combine_color_clique(coloring, cliques[0]):
                if self.valid_coloring(pc):
                    added = True
                    valid.append(pc)
            if not added:
                result = None
            else:
                for pc in valid:
                    result = self.coloring_step(cliques[1:], pc)
                    if result is not None:
                        break
        return result

    def copy_list(self, original_list):
        '''
        a method to copy a list
        Parameters:
            original_list: the list to copy (list)
        Returns:
            result: the copied list (list)
        '''
        result = []
        for element in original_list:
            result.append(copy.deepcopy(element))
        return result

    def valid_coloring(self, coloring):
        '''
        a method that determines if the coloring is valid
        Parameters:
            coloring: a list of colors in which each color is a list of nodes
                      e.g. [[1,2],[3]]
        Returns:
            valid: True if valid coloring,
                   False otherwise
        '''
        valid = False
        if coloring is not None:
            valid = True
            for color in coloring:
                for vertex in color:
                    neighbors = self.graph.neighbors(vertex)
                    for neighbor in neighbors:
                        if neighbor in color:
                            valid = False
                            break
                    if not valid:
                        break
                if not valid:
                    break
        return valid


def add_list(l1, l2, index):
    '''
    a function that  adds the list l1 to the two dimensional
    list l2
    Parameters:
        l1: the first list (list)
        l2: the second list (list of lists)
        i1: the starting index to l1 (int)
    Returns:
        new_list: the list of lists(list of lists)
    '''
    new_list = copy.deepcopy(l1)
    i = 0
    while i < len(l2):
        new_list[index] += l2[i]
        i += 1
        index += 1
    return new_list


def convert_combo(combo):
    '''
    a function that converts a combo tuple to a list
    Parameters:
        combo: a tuple of combinations (tuple)
    Returns:
        conversion: the converted combination (list)
    '''
    conversion = []
    for c in combo:
        conversion.append(c)
    return conversion


def combine_color_clique(clique, color):
    '''
    a function that takes a clique list and a color split
    and yields all the ways the clique list can be combine with coloring
    Parameters:
        clique: the clique (list of lists)
        color: the coloring (list of lists)
        index: the index
    Returns:
        coloring: the combined color (list of lists)
    '''
    color_length = len(color)
    clique_number = len(clique)
    for c in permutations(clique):
        c = convert_combo(c)
        if clique_number < color_length:
            index = 0
            while index <= color_length - clique_number:
                yield add_list(color, c, index)
                index += 1
        elif clique_number > color_length:
            index = 0
            while index <= clique_number - color_length:
                yield add_list(c, color, index)
                index += 1
        else:
            yield add_list(c, color, 0)
