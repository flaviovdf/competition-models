#-*- coding: utf8
from __future__ import division, print_function

from collections import defaultdict
from code import db

import datetime as dt
import numpy as np
import plac

MAX = 6 * 60

def get_deltas(table):

    deltas = defaultdict(lambda: defaultdict(int))
    prev_date = None
    curr_attention =defaultdict(lambda: defaultdict(int))
    prev_seen = {}

    for tstamp, user, obj in table:
        if user in prev_seen:
            curr_attention[user][obj] += min(MAX, tstamp - prev_seen[user])
        
        prev_seen[user] = tstamp
    
    deltas = curr_attention
    deltas_obj = {}
    for user in deltas:
        for obj in deltas[user]:
            if obj not in deltas_obj:
                deltas_obj[obj] = 0

            deltas_obj[obj] += deltas[user][obj]
    
    return deltas_obj

def get_transitions(table):
    
    prev = {}
    count_transitions = defaultdict(int)
    num_users_transition = defaultdict(set)
    for _, user, obj in table:
        if user in prev:
            count_transitions[user, obj, prev[user]] += 1
            num_users_transition[obj, prev[user]].add(user)
        prev[user] = obj
    
    return count_transitions, num_users_transition

def main(table_name):
    releases = {
            'Radiohead':1191974400,
            'Coldplay':1213228800,
            'Rihanna':1180573069,
            'Britney Spears':1227833869
            }

    id2name, _ = db.get_mappings(table_name)

    for artist, release_date in releases.items():
        before_after = db.filter_release(table_name, release_date)

        fbefore = open(artist + '_before_release.dat', 'w')
        fafter = open(artist + '_after_release.dat', 'w')
        
        dbefore = open(artist + '_deltas_before_release.dat', 'w')
        dafter = open(artist + '_deltas_after_release.dat', 'w')
        
        fbefore_after = [fbefore, fafter]
        dbefore_after = [dbefore, dafter]

        for i in [0, 1]:
            table = before_after[i]
            f = fbefore_after[i]
            d = dbefore_after[i]

            count_transitions, num_users_transition = get_transitions(table)
            deltas = get_deltas(table)
            print('#user destination source count', file=f)
            objs = set()
            for o1, o2 in sorted(num_users_transition):
                if len(num_users_transition[o1, o2]) >= 5:
                    for user in sorted(num_users_transition[o1, o2]):
                        if count_transitions[user, o1, o2] >= 5:
                            print(user, id2name[o1], id2name[o2], \
                                count_transitions[user, o1, o2], sep='\t',
                                file=f)
                            objs.add(o1)
                            objs.add(o2)

            print('#obj delta', file=d)
            for obj in objs:
                print(id2name[obj], deltas[obj], sep='\t', file=d)

            f.close()
            d.close()

if __name__ == '__main__':
    plac.call(main)
