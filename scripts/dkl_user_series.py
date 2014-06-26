#-*- coding: utf8
from __future__ import division, print_function

from code import db
from code import config

from collections import defaultdict
from matplotlib import pyplot as plt

import pandas as pd
import plac
import numpy as np
import os

def main(table_name, top_k_users=10, top_k_series=5, window='M'):
    id2name = db.get_mappings(table_name)[0]
    user_series = db.get_user_obj_timeseries(table_name)

    user_series_window = defaultdict(dict)
    min_stamp_user = {}
    max_stamp_user = {}
    pop_users = defaultdict(int)

    for user, obj in user_series:
        tseries = user_series[user, obj]
        w_series = tseries.resample(window, \
                    how='sum', closed='left').fillna(0)
        user_series_window[user][obj] = w_series
        pop_users[user] += w_series.values.sum()

        if user not in min_stamp_user:
            min_stamp_user[user] = w_series.index[0]
            max_stamp_user[user] = w_series.index[0]
        else:
            min_stamp_user[user] = min(min_stamp_user[user], w_series.index[0])
            max_stamp_user[user] = max(min_stamp_user[user], w_series.index[0])

    #Get the topk users 
    pop_users_vect = np.zeros(len(pop_users))
    for user in pop_users:
        pop_users_vect[user] = pop_users[user]
    top_k_users = set(pop_users_vect.argsort()[::-1][:top_k_users])
    
    #Define top k series per window
    top_series = {}
    for user in top_k_users:
        top_series[user] = set()
        idx_user = pd.date_range(min_stamp_user[user], max_stamp_user[user], \
                freq=window)
        print(idx_user)
        for idx in idx_user:
            pops = []
            for obj in user_series_window[user]:
                w_series = user_series_window[user][obj]
                if idx in w_series:
                    pops.append((w_series[idx], obj))
            
            top_k = sorted(pops)[::-1][:top_k_series]
            top_series[user].update(obj for _, obj in top_k)
    
    print(top_series)
    #Do the plots
    for user in top_series:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        to_merge = []
        names = []
        print(top_series[user])
        for obj in top_series[user]:
            to_merge.append(user_series_window[user][obj])
            names.append(id2name[obj])

        df = pd.concat(to_merge, join='outer', axis=1).fillna(0)
        df.columns = names
    
        if len(df) > 0:
            df.plot(kind='bar', stacked=True, ax=ax)
            #df.plot(ax=ax)
            #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12),
            #            ncol=df.shape[1] // 2)
            ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
            ax.set_xticklabels([x.strftime('%m/%y') for x in df.index])
            
            out_folder = config.PLOTS_FOLDER
            fpath = os.path.join(out_folder, \
                    table_name + '-' + 'user_' + str(user) + '.pdf')
            fig.savefig(fpath)
        plt.close()

if __name__ == '__main__':
    plac.call(main)
