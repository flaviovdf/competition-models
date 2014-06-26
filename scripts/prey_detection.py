#-*- coding: utf8
from __future__ import division, print_function

from code import prey
from code import db

import itertools
import numpy as np
import plac

def main(table_name, min_pop=10000):
    id2name = db.get_mappings(table_name)[0]
    series = db.get_user_obj_timeseries(table_name)
    
    good = set()
    for obj in series:
        if series[obj].values.sum() >= min_pop:
            good.add(obj)
    
    for obj1, obj2 in itertools.combinations(good, 2):
        prey.sum_prey_permutation_test()


if __name__ == '__main__':
    plac.call(main)
