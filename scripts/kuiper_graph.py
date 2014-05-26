#-*- coding: utf8
from __future__ import division, print_function
'''
Given a file with the similarity between pairs of objects,
this script will create a similarity graph. Graph creation
is performed as follows:

    1. We add an edge between A, B with weight sim(A, B)
    2. We normalize the outgoing edges of a node so sum(out(A)) == 1
    3. We filter out edges where sim(A, B) < mean + 2 * std
'''

import networkx as nx
import numpy as np
import string

def main(ids_fpath, sims_fpath):

    names = {}
    with open(ids_fpath) as names_file:
        for l in names_file:
            spl = l.split()
            names[spl[0]] = filter(lambda x: x in string.printable, \
                    ' '.join(spl[1:]))

    dg = nx.DiGraph()

    with open(sims_fpath) as sims_file:
        for l in sims_file:
            obj1, obj2, sim = l.split()
            sim = float(sim)
            if sim > 0:
                if names[obj1].strip() and names[obj2].strip():
                    dg.add_weighted_edges_from(\
                            [(names[obj1], names[obj2], sim)])
                    dg.add_weighted_edges_from(\
                            [(names[obj2], names[obj1], sim)])

    for node in dg.nodes():
        out = [x for x in dg.successors(node)] #make sure is list
        weights = np.zeros(len(out), dtype='f')
    
        for i, n in enumerate(out):
            w = dg.get_edge_data(node, n)['weight']
            weights[i] = w

        weights /= weights.sum()
        mean = weights.mean()
        std = weights.std()

        for i, n in enumerate(out):
            dg.remove_edge(node, n)
            if weights[i] > mean + 2 * std:
                dg.add_weighted_edges_from([(node, n, weights[i])])

    nx.write_gexf(dg, 'graph.gexf')

if __name__ == '__main__':
    plac.call(main)
