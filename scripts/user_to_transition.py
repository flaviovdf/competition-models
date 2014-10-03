#-*- coding: utf8
from __future__ import division, print_function

from collections import defaultdict
from code import db

import numpy as np
import plac

def main(table_name):
    
    id2name, _ = db.get_mappings(table_name)

    user_pop = defaultdict(int)
    obj_pop = defaultdict(int)
    for _, user, obj in db.iter_sorted(table_name):
        user_pop[user] += 1
        obj_pop[obj] += 1
    
    user_pop_arr = np.zeros(len(user_pop))
    obj_pop_arr = np.zeros(len(obj_pop))
    
    for user in user_pop:
        user_pop_arr[user] = user_pop[user]

    for obj in obj_pop:
        obj_pop_arr[obj] = obj_pop[obj]

    top_100_users = set(user_pop_arr.argsort()[::-1][:100])
    top_100_obj = set(obj_pop_arr.argsort()[::-1][:100])

    prev = {}
    count_transitions = defaultdict(int)
    for _, user, obj in db.iter_sorted(table_name):
        if user in top_100_users and user in prev and obj in top_100_obj:
            count_transitions[user, obj, prev[user]] += 1
        prev[user] = obj

    for user, o1, o2 in sorted(count_transitions):
        print(user, 'dest='+id2name[o1], 'source='+id2name[o2], \
                count_transitions[user, o1, o2], sep='\t')

if __name__ == '__main__':
    plac.call(main)
