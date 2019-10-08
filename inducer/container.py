"""
-------------------------------------------------------
contains
holds a function contains
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-17
-------------------------------------------------------
"""
import itertools
import networkx as nx


def induced_subgraph(G, H):
    '''
    induced_subgraph
    a function that checks if G has an induced subgraph of H
    Parameters:
        G: the graph to check (networkx)
        H: the induced subgraph (networkx)
    Returns:
        induced: the induced subgraph (networkx)
    Method:
        just create every permutation of the G graph with as many vertices
        as H and use networkx to check if isomorphic
    Note:
         not solved in polynomial time (only use for small cases)
    '''
    n = len(G)
    k = len(H)
    if n < k:
        return None
    permutations = create_permutations(n, k)
    induced = None
    for subset in permutations:
        subgraph = G.subgraph(subset)
        if nx.faster_could_be_isomorphic(subgraph, H):
            if nx.is_isomorphic(subgraph, H):
                induced = subgraph
                # only want to find one
                break
    return induced


def create_permutations(n, k):
    '''
    create_permutations
    a function which returns a list of all possible permutations n choose k
    Parameters:
        n: the total number of items
        k: the number of items to choose
    Returns:
        iterator: to the list of permutations
    '''
    number_list = []
    for x in range(0, n):
        number_list.append(x)
    return itertools.combinations(number_list, k)


def k_vertex(g, subgraphs):
    '''
    k_vertex
    a function that finds all the k_vertex for k=0 to n (# of g vertices)
    Parameters:
        g: the graph to finds the k vertex for (networkx)
        subgraphs: the list of subgraphs g is to be free of (list of networkx)
    Returns:
        k_vertexes: python dictionary
        eg. [{has_k_vertex: Boolean, combination: [[node,node],[node,node]]}]
    '''
    nodes = g.nodes()
    node = len(g.nodes())
    k_vertexes = []
    # check for zero vertex
    g.add_node(node)
    zero_vertex = True
    for sub in subgraphs:
        induced = induced_subgraph(g, sub)
        if induced is not None:
            zero_vertex = False
            break
    if zero_vertex:
        k_vertexes.append({'has_k_vertex': True, 'combinations': []})
    else:
        k_vertexes.append({'has_k_vertex': False, 'combinations': []})
    # check the rest now
    g.remove_node(node)  # remove added node
    for k in range(1, node + 1):
        k_vertexes.append({'has_k_vertex': False, 'combinations': []})
        for combo in itertools.combinations(nodes, k):
            g.add_node(node)  # add node
            # add the edges
            for vertex in combo:
                g.add_edge(node, vertex)
            # assume it does not contain all the subgraphs
            does_contain = False
            for sub in subgraphs:
                induced = induced_subgraph(g, sub)
                if induced is not None:
                    # does contain a forbidden subgraph
                    does_contain = True
            if not does_contain:
                # did not contain any forbidden subgraph
                k_vertexes[k]['has_k_vertex'] = True
                k_vertexes[k]['combinations'].append(combo)
            g.remove_node(node)  # remove added node and its edges
    return k_vertexes
