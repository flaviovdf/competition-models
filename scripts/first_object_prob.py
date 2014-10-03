#-*- coding: utf8
from __future__ import division, print_function

from code import config
from code import db

from collections import defaultdict

import datetime as dt
import numpy as np
import pandas as pd
import plac

def filter_release(table_name, obj, release_date, delta_str='60D'):
    
    delta = float(pd.to_timedelta(delta_str) / 1e9)
    
    before_start = release_date - delta
    after_end = release_date + delta
    
    query = '(date > %f) & (date <= %f)'
    
    before = query % (before_start, release_date)
    after = query % (release_date, after_end)
    
    before_release = [x for x in db.iter_sorted(table_name, before)]
    after_release = [x for x in db.iter_sorted(table_name, after)]
    
    return before_release, after_release

def play_position(trace, obj_interest):

    counter = defaultdict(int)
    
    prev_date = dt.date.fromtimestamp(trace[0][0])
    user_pos = {}
    prev_obj = {}

    for tstamp, user, obj in trace:
        
        date = dt.date.fromtimestamp(tstamp)
        changed = False
        if date != prev_date:
            user_pos = {}
            prev_obj = {}

        if user not in user_pos:
            user_pos[user] = 0
            changed = True

        if user in prev_obj and obj != prev_obj[user]:
            user_pos[user] += 1
            changed = True

        if changed and obj == obj_interest:
            counter[user_pos[user]] += 1
        
        prev_obj[user] = obj
    
    return counter


def main():
    releases = {
            'Radiohead':1191974400,
            #'Coldplay':1213228800,
            #'Rihanna':1180573069,
            #'Britney Spears':1227833869
            }

    obj_name = 'Radiohead'
    id2name, name2id = db.get_mappings('lastfm_artist')
    before, after = filter_release('lastfm_artist', name2id[obj_name], \
            releases[obj_name])

    counter_before_plays = play_position(before, name2id[obj_name])
    counter_after_plays = play_position(after, name2id[obj_name])

    users_before = len(set([u for _, u, _ in before]))
    users_after = len(set([u for _, u, _ in after]))
    
    print('Before', ' '.join([(k, v) for k, v in counter_before_plays.items()]))
    print('After', ' '.join([(k, v) for k, v in counter_before_after.items()]))

if __name__ == '__main__':
    plac.call(main)
