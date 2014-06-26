#!/usr/bin/env python
# -*- coding: utf8

from __future__ import division, print_function

from code import config
from code import db
from code.plot_helper import initialize_matplotlib
from code.plot_helper import three_plots

from collections import defaultdict

import numpy as np
import os
import plac
 
def main(table_name):
   
    initialize_matplotlib()

    obj_to_users = defaultdict(set)
    obj_count = defaultdict(int)
    duplicate_counts = defaultdict(int)
    audience_counts = defaultdict(int)
    
    for _, user, obj in db.iter_sorted(table_name):
        if user in obj_to_users[obj]:
            duplicate_counts[obj] += 1
        else:
            audience_counts[obj] += 1
            
        obj_to_users[obj].add(user)
        obj_count[obj] += 1
    
    out_folder = config.PLOTS_FOLDER
    fname = os.path.join(out_folder, '%s-pop.pdf' % table_name)
    three_plots(obj_count.values(), r'Popularity', fname)
    
    fname = os.path.join(out_folder, '%s-audi.pdf' % table_name)
    three_plots(audience_counts.values(), r'Audience', fname)
    
    revisits_over_audience = np.zeros(len(obj_count))
    for obj in obj_count:
        revisits_over_audience[obj] = \
                duplicate_counts[obj] / audience_counts[obj]
    
    fname = os.path.join(out_folder, '%s-rev-over-audi.pdf' % table_name)
    three_plots(revisits_over_audience, r'Returning/Audience (binned)', \
            fname, False)

if __name__ == '__main__':
    plac.call(main)
