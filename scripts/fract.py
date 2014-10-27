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
   
    obj_count = defaultdict(int)
    for _, user, obj in db.iter_sorted(table_name):
        obj_count[obj] += 1
    
    x = np.zeros(len(obj_count))
    for o in obj_count:
        x[o] = obj_count[o]
    
    for i in xrange(1, 4):
        print(i, x[x <= i].sum() / x.sum())

if __name__ == '__main__':
    plac.call(main)
