#!/usr/bin/env python
# -*- coding: utf8

from __future__ import division, print_function

from code import config
from code import db

from collections import defaultdict

from matplotlib import pyplot as plt
from matplotlib import rc

import numpy as np
import os
import plac

def initialize_matplotlib(): 
    inches_per_pt = 1.0 / 72.27 
    golden_mean = (np.sqrt(5) - 1.0) / 2.0 
    
    fig_width = 2 * 240.0 * inches_per_pt
    #fig_height = .25 * fig_width
    fig_height = fig_width

    rc('axes', labelsize=8) 
    rc('axes', titlesize=7) 
    rc('axes', unicode_minus=False) 
    rc('axes', grid=False) 
    rc('figure', figsize=(fig_width, fig_height)) 
    rc('grid', linestyle=':') 
    rc('font', family='serif') 
    rc('legend', fontsize=8) 
    rc('lines', linewidth=1) 
    rc('ps', usedistiller='xpdf') 
    rc('text', usetex=True) 
    rc('xtick', labelsize=7) 
    rc('ytick', labelsize=7)
    rc('xtick', direction='out') 
    rc('ytick', direction='out')

def main(table_name):
   
    initialize_matplotlib()

    users_to_object = defaultdict(set)
    user_count = defaultdict(int)
    
    for _, user, obj in db.iter_sorted(table_name):
        users_to_object[user].add(obj)
        user_count[user] += 1
   
    x = np.zeros(len(users_to_object))
    y = np.zeros(len(users_to_object))
    for user in users_to_object:
        x[user] = user_count[user]
        y[user] = len(users_to_object[user])

    out_folder = config.PLOTS_FOLDER
    fname = os.path.join(out_folder, '%s-variety.pdf' % table_name)
    
    plt.loglog(x, x, 'k-')
    plt.loglog(x, y, 'wo')
    
    plt.xlabel('Num plays')
    plt.ylabel('Number of unique artists')

    plt.savefig(fname)

if __name__ == '__main__':
    plac.call(main)
