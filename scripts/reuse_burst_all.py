#-*- coding: utf8
from __future__ import division, print_function

from bisect import bisect_left
from bisect import bisect_right

from collections import deque
from collections import OrderedDict

from code import db
from code import plot_helper

import numpy as np
import pandas as pd
import plac

def get_counts(table_name, maxlen=2):
    
    user_queue = {}
    counts = {}
    
    unique_users = {}
    audience = {}

    for tstamp, user, obj in db.iter_sorted(table_name):
        if user not in user_queue:
            user_queue[user] = deque(maxlen=maxlen)

        d = user_queue[user]
        d.append(obj)
        
        if obj not in audience:
            unique_users[obj] = set()
            audience[obj] = OrderedDict()
        
        unique_users[obj].add(user)
        audience[obj] = len(unique_users[obj])

        if len(d) == maxlen: 
            assert d[-1] == obj
            mem = frozenset(d[x] for x in range(len(d) - 1))
            
            if obj not in counts:
                counts[obj] = {}

            if mem not in counts[obj]:
                counts[obj][mem] = 0

            counts[obj][mem] += 1
    
    return counts, audience

def main(table_name, maxlen=2):
    
    maxlen = int(maxlen)

    id2name, name2id = db.get_mappings(table_name)
    counts, audience = get_counts(table_name, maxlen)
    
    for obj in counts:
        obj_name = id2name[obj]
        sum_ = sum(counts[obj].values())
        
        for mem in counts[obj]:
            
            #if counts[obj][mem] < 100:
            #    continue

            if obj in mem:
                continue

            print('P[', obj_name, '|', \
                    ','.join(id2name[x] for x in mem), \
                    ']',
                    counts[obj][mem])

if __name__ == '__main__':
    plac.call(main)
