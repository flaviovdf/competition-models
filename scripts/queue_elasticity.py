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

def get_counts(table_name):
    
    audience = {}
    plays = {}
    unique_users = {}
    last_seen = {}

    for tstamp, user, obj in db.iter_sorted(table_name):
        
        if user not in plays:
            plays[user] = OrderedDict()
            count = 0
        else:
            last_stamp = last_seen[user]
            count = plays[user][last_stamp]
        
        plays[user][tstamp] = count + 1
        
        if obj not in audience:
            unique_users[obj] = set()
            audience[obj] = OrderedDict()
        
        unique_users[obj].add(user)
        audience[obj][tstamp] = set(unique_users[obj])
        last_seen[user] = tstamp

    return plays, audience

def main(table_name, delta_str='1D'):
    
    delta = float(pd.to_timedelta(delta_str) / 1e9)
    id2name, name2id = db.get_mappings(table_name)
    
    stamped_plays, stamped_audience = get_counts(table_name)
    
    releases = {'Radiohead':[1191974400],
                'Coldplay':[1213228800],
                'Rihanna':[1180573069],
                'Britney Spears':[1227833869]
                }

    for obj_name in releases:
        obj = name2id[obj_name]

        for release_date in releases[obj_name]:

            plays_before = []
            plays_during = []
            plays_after = []

            audience = stamped_audience[obj]
            
            stamps = audience.keys()
            before = bisect_left(stamps, release_date - delta)
            after = bisect_right(stamps, release_date + delta)
                
            if before >= len(stamps) or after >= len(stamps) or \
                    before == after:
                continue

            stamp_before = stamps[before]
            stamp_after = stamps[after]
            audience_before = audience[stamp_before]

            for user in audience_before:
                stamps_user = plays[user].keys()
                before_user = bisect_left(stamps_user, release_date - delta)
                after_user = bisect_right(stamps_user, release_date - delta)
                
                if before_user >= len(stamps_user) or \
                        after_user >= len(stamps_user) or \
                        before_user == after_user:
                    continue
                
                plays_before.append(plays[user][stamps_user[before_user]])
                plays_after.append(plays[user][stamps_user[after_user]])
                plays_during.append(plays_after[-1] - plays_before[-1])
            
            plot_helper.three_plots(plays_before, 'Plays before release', \
                    obj_name + '-before.pdf')
            plot_helper.three_plots(plays_during, 'Plays during release', \
                    obj_name + '-after.pdf')
            plot_helper.three_plots(plays_after, 'Plays after release', \
                    obj_name + '-before.pdf')


if __name__ == '__main__':
    plac.call(main)
