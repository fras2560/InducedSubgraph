'''
Created on Sep 10, 2015

@author: Dallas
'''
from networkx.algorithms import graph_clique_number
from networkx import complement
from inducer.helper import make_cycle
from inducer.container import induced_subgraph


def even_hole_free(G):
    i_set = graph_clique_number(complement(G))
    free = None
    i = 4
    while i <= i_set * 2 and free is None:
        g = make_cycle(i)
        induced = induced_subgraph(G, g)
        if induced is not None:
            free = induced
        i += 2
    return free


def odd_hole_free(G):
    i_set = graph_clique_number(complement(G))
    free = None
    i = 5
    while i <= i_set * 2 + 1 and free is None:
        g = make_cycle(i)
        induced = induced_subgraph(G, g)
        if induced is not None:
            free = induced
        i += 2
    return free
