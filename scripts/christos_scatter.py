#-*- coding: utf8
from __future__ import division, print_function

import matplotlib
matplotlib.use('Agg')

from collections import defaultdict
from collections import OrderedDict

from code import db

from matplotlib import rc
from matplotlib import pyplot as plt

import datetime as dt
import pandas as pd
import numpy as np

MAX = 6 * 60

def get_deltas(trace, obj_interest, complement=False):

    deltas = OrderedDict()
    prev_date = None
    curr_attention = None

    for tstamp, user, obj in trace:
         
        if user not in deltas:
            deltas[user] = 0

        date = dt.date.fromtimestamp(tstamp)
        if prev_date is None or prev_date != date:
            prev_date = date
            prev_seen = {}

            if curr_attention is not None:
                for seen_user in curr_attention:
                    deltas[seen_user] += curr_attention[seen_user]

            curr_attention = defaultdict(int)

        if user in prev_seen:
            curr_attention[user] += min(MAX, tstamp - prev_seen[user])
        
        if (not complement and obj == obj_interest) or \
                (complement and obj != obj_interest):
            prev_seen[user] = tstamp
        else:
            if user in prev_seen:
                del prev_seen[user]
    
    return deltas

def get_before_after(attention_others, attention_obj, users_to_consider):

    values_obj = []
    values_others = []
                
    for user in users_to_consider:
        values_obj.append(attention_obj[user])
        values_others.append(attention_others[user])
                                            
    return np.asarray(values_obj), np.asarray(values_others)

def christos_scatter(before, after, obj):
    
    attention_others_before = get_deltas(before, obj, True)
    attention_others_after = get_deltas(after, obj, True)
    
    attention_obj_before = get_deltas(before, obj, False)
    attention_obj_after = get_deltas(after, obj, False)

    users_of_interest = sorted([user \
            for user in attention_obj_before \
            if attention_obj_before[user] and \
            user in attention_obj_after and attention_obj_after[user]])
    
    print(len(users_of_interest))

    from_values_obj, from_values_others = \
            get_before_after(attention_others_before, attention_obj_before, \
            users_of_interest)

    to_values_obj, to_values_others = \
            get_before_after(attention_others_after, attention_obj_after, \
            users_of_interest)
    
    plt.plot(from_values_others, from_values_obj, 'go', markersize=10, label='Before')
    plt.plot(to_values_others, to_values_obj, 'ro', markersize=10, label='After')
    
    plt.ylabel('Number of seconds dedicate to artist')
    plt.xlabel('Number of seconds dedicate to everyone else')
    plt.legend()
    
    for i in xrange(len(from_values_obj)):
        x = [from_values_others[i], to_values_others[i]]
        y = [from_values_obj[i], to_values_obj[i]]
        plt.plot(x, y, 'k-')

    ax = plt.gca()
    
    ax.set_xlim((1, 1e7))
    ax.set_ylim((1, 1e7))
    
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig('before_after_scatter.png')
    plt.close()

def simple_smooth(x, y, n_bins=5, invert=False):
    
    if not invert:
        idx_sorted = x.argsort()
    else:
        idx_sorted = y.argsort()
        
    bin_size = int(idx_sorted.shape[0] / n_bins)
    
    mean_x = []
    mean_y = []
    
    median_x = []
    median_y = []
    
    for j in range(0, idx_sorted.shape[0], bin_size):
        idx = idx_sorted[j:j+bin_size]
        mean_x.append(x[idx].mean())
        mean_y.append(y[idx].mean())
        
        median_x.append(np.median(x[idx]))
        median_y.append(np.median(y[idx]))
    
    S = np.zeros(shape=(len(mean_x), 4))
    
    S[:, 0] = mean_x
    S[:, 1] = mean_y
    S[:, 2] = median_x
    S[:, 3] = median_y
    
    return S

def christos_scatter_smooth(before, after, obj, invert=False): 
    
    attention_others_before = get_deltas(before, obj, True)
    attention_others_after = get_deltas(after, obj, True)
    
    attention_obj_before = get_deltas(before, obj, False)
    attention_obj_after = get_deltas(after, obj, False)

    users_of_interest = sorted([user \
            for user in attention_obj_before \
            if attention_obj_before[user] and \
            user in attention_obj_after and attention_obj_after[user]])
    
    from_values_obj, from_values_others = \
            get_before_after(attention_others_before, attention_obj_before, \
            users_of_interest)

    to_values_obj, to_values_others = \
            get_before_after(attention_others_after, attention_obj_after, \
            users_of_interest)

    from_lowess = simple_smooth(from_values_others, from_values_obj, \
            invert=invert)
    to_lowess = simple_smooth(to_values_others, to_values_obj, \
            invert=invert)

    plt.plot(from_lowess[:, 2], from_lowess[:, 3], 'go', label='Before')
    plt.plot(to_lowess[:, 2], to_lowess[:, 3], 'ro', label='After')
            
    plt.quiver(from_lowess[:, 2], from_lowess[:, 3], \
            to_lowess[:, 2] - from_lowess[:, 2], \
            to_lowess[:, 3] - from_lowess[:, 3], angles='xy', \
            scale_units='xy', scale=1, width=.0018)
                    
    plt.ylabel('Number of seconds dedicate to artist')
    plt.xlabel('Number of seconds dedicate to everyone else')
    plt.legend()
                                
    ax = plt.gca()
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    #ax.set_xlim(1, 1e7)
    #ax.set_ylim(1, 1e7)

    plt.savefig('before_after_scatter.png')
    plt.close()


def main():
    releases = {
            'Radiohead':1191974400,
            #'Coldplay':1213228800,
            #'Rihanna':1180573069,
            #'Britney Spears':1227833869
            }

    rc('figure', figsize=(12, 12))
    
    obj_name = 'Radiohead'
    id2name, name2id = db.get_mappings('lastfm_artist')
    before, after = db.filter_release('lastfm_artist', releases[obj_name])
    
    christos_scatter(before, after, name2id[obj_name])
    christos_scatter_smooth(before, after, name2id[obj_name])

if __name__ == '__main__':
    main()
