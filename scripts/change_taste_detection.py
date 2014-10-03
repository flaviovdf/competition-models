#-*- coding: utf8
from __future__ import division, print_function

from collections import defaultdict

from code import prey
from code import db

import itertools
import numpy as np
import pandas as pd
import plac

def get_topk(tseries, window_size, top_k=.01):
    pops = np.zeros(len(tseries))
    for obj in tseries:
        pops[obj] = tseries[obj].values.sum()
                            
    reverse_sort = pops.argsort()[::-1]
    to_choose = int(reverse_sort.shape[0] * top_k)
    
    return set(x for x in reverse_sort[:to_choose])

def get_obj_to_users(user_obj_series):
    index = defaultdict(set)
    for user, obj in user_obj_series:
        index[obj].add(user)

    return index

def resample_obj(series_dict, window_size, top_k_objs):
    return_val = {}
    for obj in series_dict:
        if obj in top_k_objs:
            return_val[obj] = \
                    series_dict[obj].resample(window_size, \
                            how='sum', closed='left').fillna(0)
    return return_val

def resample_user_obj(series_dict, window_size, top_k_objs):
    return_val = {}
    for user, obj in series_dict:
        if obj in top_k_objs:
            return_val[user, obj] = \
                    series_dict[user, obj].resample(window_size, \
                            how='sum', closed='left').fillna(0)
    return return_val

def main(table_name, window_size='1w', min_users=20, mean_past=False):
    
    min_users = int(min_users)
    mean_past = bool(mean_past)
    
    print('#Tests for:', table_name, window_size, min_users, mean_past)
    print('#Loading time stamps...')
    id2name, name2id = db.get_mappings(table_name)
    obj_series = db.get_obj_timeseries(table_name)
    user_obj_series = db.get_user_obj_timeseries(table_name)
    print('#Loaded...')
   
    top_k_objs = get_topk(obj_series, id2name)
    
    #resample series
    print('#Resampling %d series...' % len(top_k_objs))
    obj_series = resample_obj(obj_series, window_size, top_k_objs)
    user_obj_series = resample_user_obj(user_obj_series, window_size, \
            top_k_objs)
    
    #get user to obj index
    obj_to_user_index = get_obj_to_users(user_obj_series)
    
    print('#Testing for prey behavior on window sizes of', window_size, '...')
    for obj1, obj2 in itertools.combinations(obj_to_user_index.keys(), 2):
        users1 = obj_to_user_index[obj1]
        users2 = obj_to_user_index[obj2]
        
        intersect = users1.intersection(users2)
        if len(intersect) < min_users:
            continue
        
        to_concat1 = {}
        to_concat2 = {}
        for user in intersect:
            to_concat1[user] = user_obj_series[user, obj1]
            to_concat2[user] = user_obj_series[user, obj2]

        uframe1 = pd.concat(to_concat1, join='outer', axis=1).fillna(0) 
        uframe2 = pd.concat(to_concat2, join='outer', axis=1).fillna(0)
        index = uframe1.index.intersection(uframe2.index)
       
        uframe1 = uframe1.reindex(index, fill_value=0)
        uframe2 = uframe2.reindex(index, fill_value=0)
        
        #Time by users matrix
        obj1_mat = uframe1.values
        obj2_mat = uframe2.values
        
        print('#Testing:', id2name[obj1], 'vs', id2name[obj2])
        for window in xrange(1, obj1_mat.shape[0]):
            
            prev = window - 1
            now = window
            
            if not mean_past:
                values1_prev = obj1_mat[prev]
                values2_prev = obj2_mat[prev]
            else:
                values1_prev = obj1_mat[:now].mean(axis=0)
                values2_prev = obj2_mat[:now].mean(axis=0)

            values1_now = obj1_mat[now]
            values2_now = obj2_mat[now]

            pval1_obj1_vs_obj2, pval2_obj1_vs_obj2 = \
                    prey.evidence_prey(values1_now, values1_prev, \
                    values2_now, values2_prev)

            pval1_obj2_vs_obj1, pval2_obj2_vs_obj1 = \
                    prey.evidence_prey(values2_now, values2_prev, \
                    values1_now, values1_prev)
            
            print(index[now], \
                    pval1_obj1_vs_obj2, pval2_obj1_vs_obj2,
                    pval1_obj2_vs_obj1, pval2_obj2_vs_obj1, sep='\t')

if __name__ == '__main__':
    plac.call(main)
