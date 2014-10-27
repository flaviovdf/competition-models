#-*- coding: utf8
from __future__ import division, print_function

from collections import defaultdict
from code import db

import numpy as np
import plac

def main(table_name, min_count_users, min_count_transitions):
    
    min_count_users = int(min_count_users)
    min_count_transitions = int(min_count_transitions)

    id2name, _ = db.get_mappings(table_name)

    prev = {}
    count_transitions = defaultdict(int)
    num_users_transition = defaultdict(set)
    for _, user, obj in db.iter_sorted(table_name):
        if user in prev:
            count_transitions[user, obj, prev[user]] += 1
            num_users_transition[obj, prev[user]].add(user)
        prev[user] = obj

    print('#user destination source count')
    for o1, o2 in sorted(num_users_transition):
        if len(num_users_transition[o1, o2]) >= min_count_users:
            for user in sorted(num_users_transition[o1, o2]):
                if count_transitions[user, o1, o2] >= min_count_transitions:
                    print(user, id2name[o1], id2name[o2], \
                        count_transitions[user, o1, o2], sep='\t')

if __name__ == '__main__':
    plac.call(main)
