#-*- coding: utf8
'''
Plots the inter-arrival time for users, objects or (user, object) pairs.
'''
from __future__ import division, print_function

from code import db
from code.config import PLOTS_FOLDER
from code.plot_helper import initialize_matplotlib
from code.plot_helper import three_plots

from matplotlib import pyplot as plt

import os
import numpy as np
import plac
import powerlaw

OPTS = ['user', 'obj', 'pair']

def main(table_name, what):
    
    if what not in OPTS:
        raise Exception('Choose what from: ' + ' '.join(OPTS))

    initialize_matplotlib()
    
    seen = {}
    deltas = []
    
    for tstamp, user, obj in db.iter_sorted(table_name):
        if what == 'user':
            key = user
        elif what == 'obj':
            key = obj
        else:
            key = (user, obj)
        
        if key in seen:
            delta = tstamp - seen[key]
            deltas.append(delta)
        seen[key] = tstamp
   
    deltas = np.asarray(deltas, dtype='i')
    fpath = os.path.join(PLOTS_FOLDER, table_name + '-' + what + '_interarrival.pdf')
    three_plots(deltas, r'$\delta$ between access for ' + what, fpath, \
            discrete=True)
    
if __name__ == '__main__':
    plac.call(main)
