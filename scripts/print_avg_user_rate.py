#-*- coding: utf8
'''
Prints the average rate of an user to an object
'''
from __future__ import division, print_function

from code import db
from collections import defaultdict

import numpy as np
import plac

def main(table_name, min_pop=10000):

    counts = defaultdict(int)
    obj_pop = defaultdict(int)
    last_stamp = {}
    first_stamp = {}

    for tstamp, user, obj in db.iter_sorted(table_name):
        if (user, obj) not in first_stamp:
            first_stamp[user, obj] = tstamp

        obj_pop[obj] += 1
        counts[user, obj] += 1
        last_stamp[user, obj] = tstamp
    
    for obj in obj_pop.keys(): #no concurrent, keys is a copy
        if obj_pop[obj] < min_pop:
            del obj_pop[obj]
    
    rates = defaultdict(list)
    for user, obj in sorted(counts.keys()):
        if obj not in obj_pop:
            continue

        delta = last_stamp[user, obj] - first_stamp[user, obj]
        if delta == 0:
            continue
        
        rates[obj].append(counts[user, obj] / delta)

    for obj in rates:
        print(obj, ' '.join([str(x) for x in rates[obj]]))

if __name__ == '__main__':
    plac.call(main)
