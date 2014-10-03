#-*- coding: utf8
from __future__ import division, print_function

import matplotlib
matplotlib.use('Agg')

from code import config
from code import db

from matplotlib import pyplot as plt
from matplotlib import rc

from collections import defaultdict
from statsmodels.distributions.empirical_distribution import ECDF

import datetime as dt
import numpy as np
import pandas as pd
import plac

MAX = 6 * 60
DAY = 24 * 60 * 60
def plot_dist(data, ax_data, ax_cdf, style_data, style_cdf, label_data, label_cdf, discrete=True):
    
    data = np.asanyarray(data)
    data = data[data > 0]

    ecdf = ECDF(data)

    n = data.shape[0]
    
    log_min_size = np.log10(data.min())
    log_max_size = np.log10(data.max())
    nbins = np.ceil((log_max_size - log_min_size) * min(n, 10))
    bins = np.unique(np.floor(np.logspace(log_min_size, log_max_size, nbins)))
    
    hist, edges = np.histogram(data, bins)
    x = (edges[1:] + edges[:-1]) / 2.0
    
    if not x.any():
        return
    
    if discrete:
        counts = np.bincount(data)
        xvals = np.arange(counts.shape[0]) + 1
        ax_data.loglog(xvals, counts, style_data, label=label_data)
    else:
        ax_data.loglog(x, hist, style_data, label=label_data)

    ax_cdf.loglog(x, 1 - ecdf(x), style_cdf, label=label_cdf)

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

def get_deltas(trace, obj_interest):

    deltas = []
    prev_date = None
    curr_attention = None

    for tstamp, user, obj in trace:
        date = dt.date.fromtimestamp(tstamp)
        if prev_date is None or prev_date != date:
            prev_date = date
            prev_seen = {}

            if curr_attention is not None:
                deltas.extend(curr_attention.values())

            curr_attention = defaultdict(int)

        if user in prev_seen:
            curr_attention[user] += min(MAX, tstamp - prev_seen[user])

        if obj == obj_interest:
            prev_seen[user] = tstamp
        else:
            if user in prev_seen:
                del prev_seen[user]
    
    return np.asarray(deltas, dtype='i')

def main():
    releases = {
            'Radiohead':1191974400,
            #'Coldplay':1213228800,
            #'Rihanna':1180573069,
            #'Britney Spears':1227833869
            }

    rc('figure', figsize=(12, 6))
    
    obj_name = 'Radiohead'
    id2name, name2id = db.get_mappings('lastfm_artist')
    before, after = filter_release('lastfm_artist', name2id[obj_name], \
            releases[obj_name])
    
    deltas_before = get_deltas(before, name2id[obj_name])
    deltas_after = get_deltas(after, name2id[obj_name])
    
    ax_data = plt.subplot(121)
    ax_cdf = plt.subplot(122)

    plot_dist(deltas_before, ax_data, ax_cdf, 'go', 'g-', 'Before Release', \
            'Before Release', discrete=False)
        
    plot_dist(deltas_after, ax_data, ax_cdf, 'bo', 'b-', 'After Release', \
            'After Release', discrete=False)
                                    
    ax_data.set_xlabel('Seconds dedicated to radiohead per day')
    ax_data.set_ylabel('Count')

    ax_cdf.set_xlabel('Seconds dedicated to radiohead per day')
    ax_cdf.set_ylabel('CCDF')
    ax_cdf.legend(loc='lower left')
    
    plt.tight_layout(pad=0)
    
    plt.savefig('attention_radiohead.pdf')
    plt.close()

    np.savetxt('attention_before.txt', deltas_before)
    np.savetxt('attention_after.txt', deltas_after)

if __name__ == '__main__':
    plac.call(main)
