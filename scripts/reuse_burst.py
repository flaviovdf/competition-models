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
    prev_seen = {}
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
        audience[obj][tstamp] = len(unique_users[obj])

        if len(d) == maxlen: 
            assert d[-1] == obj
            mem = frozenset(d[x] for x in range(len(d) - 1))
            
            if (obj, mem) in prev_seen:
                prev_tstamp = prev_seen[obj, mem]
                prev_count = counts[obj][mem][prev_tstamp]
            else:
                prev_count = 0
            
            if obj not in counts:
                counts[obj] = {}

            if mem not in counts[obj]:
                counts[obj][mem] = OrderedDict()

            prev_seen[obj, mem] = tstamp
            counts[obj][mem][tstamp] = prev_count + 1
    
    return counts, audience

def main(table_name, maxlen=2, delta_str='1D'):
    
    maxlen = int(maxlen)
    delta = float(pd.to_timedelta(delta_str) / 1e9)

    id2name, name2id = db.get_mappings(table_name)
    stamped_counts, stamped_audience = get_counts(table_name, maxlen)
    
    releases = {'Radiohead':[1191974400],
                'Coldplay':[1213228800],
                'Rihanna':[1180573069],
                'Britney Spears':[1227833869]
                }

    for obj_name in releases:
        obj = name2id[obj_name]
        
        for release_date in releases[obj_name]:
             
            mem_counts_before = {}
            mem_counts_during = {}
            mem_counts_after = {}
            
            for memory in stamped_counts[obj]:

                stamps = stamped_counts[obj][memory].keys()    
                before = bisect_left(stamps, release_date - delta)
                after = bisect_right(stamps, release_date + delta)
                
                if before >= len(stamps) or after >= len(stamps) or \
                        before == after:
                    continue

                stamp_before = stamps[before]
                stamp_after = stamps[after]
                stamp_last = stamps[-1]

                mem_counts_before[memory] = \
                        stamped_counts[obj][memory][stamp_before]

                mem_counts_after[memory] = \
                        stamped_counts[obj][memory][stamp_last] - \
                        stamped_counts[obj][memory][stamp_after]
                
                mem_counts_during[memory] = \
                        stamped_counts[obj][memory][stamp_after] - \
                        mem_counts_before[memory]
            
            sum_before = sum(mem_counts_before.values())
            sum_during = sum(mem_counts_during.values())
            sum_after = sum(mem_counts_after.values())

            before_objs = sorted(mem_counts_before, key=mem_counts_before.get, \
                    reverse=True)[:10]
            during_objs = sorted(mem_counts_during, key=mem_counts_during.get, \
                    reverse=True)[:10]
            after_objs = sorted(mem_counts_after, key=mem_counts_after.get, \
                    reverse=True)[:10]
            
            #Get audience data
            stamps = stamped_audience[obj].keys()
            before = bisect_left(stamps, release_date - delta)
            after = bisect_right(stamps, release_date + delta)
            
            stamp_before = stamps[before]
            stamp_after = stamps[after]

            audience_before = stamped_audience[obj][stamp_before]
            audience_after = stamped_audience[obj][stamp_after]

            print(obj_name, 'had a release on', release_date)
            print(audience_before, 'listened', delta_str, 'before the release')
            print('It increased to:', audience_after, delta_str, 'after release')
            print()
            print('Transition probabilities up to', delta_str, 'before release')
            print('Computed based on total #plays of', sum_before)
            for mem in before_objs:
                print('P[', obj_name, '|', \
                        ','.join(id2name[x] for x in mem), \
                        ']',
                        mem_counts_before[mem] / sum_before)
            print()
            
            print('Transition probabilities', delta_str, 'around the release')
            print('Computed based on total #plays of', sum_during)
            for mem in during_objs:
                print('P[', obj_name, '|', \
                        ','.join(id2name[x] for x in mem), \
                        ']',
                        mem_counts_during[mem] / sum_during)
            print()
            
            print('Transition probabilities from', delta_str, \
                    'after the release')
            print('Computed based on total #plays of', sum_after)
            for mem in after_objs:
                print('P[', obj_name, '|', \
                        ','.join(id2name[x] for x in mem), \
                        ']',
                        mem_counts_after[mem] / sum_after)
            print('---')
            print()
            print()
            print('---')

if __name__ == '__main__':
    plac.call(main)
