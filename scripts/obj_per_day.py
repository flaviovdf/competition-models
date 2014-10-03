#-*- coding: utf8
from __future__ import division, print_function

from code import db
from code.config import PLOTS_FOLDER
from code.plot_helper import initialize_matplotlib
from code.plot_helper import three_plots

import os
import numpy as np
import pandas as pd
import plac

def resample(user_tseries):
    rv = {}
    idx = {}
    for user, obj in user_tseries:
        if user not in idx:
            idx[user] = set()

        rv[user, obj] = user_tseries[user, obj].resample('1d', how='sum', \
                closed='left').fillna(0)
        idx[user].add(obj)
    return idx, rv

def main(table_name):
    
    initialize_matplotlib()

    user_obj_tseries = db.get_user_obj_timeseries(table_name)
    idx_user_to_objs, user_obj_tseries = resample(user_obj_tseries)
    

    values = []
    for user in idx_user_to_objs:
        objs = idx_user_to_objs[user]
        to_concat = dict((obj, user_obj_tseries[user, obj]) for obj in objs)
        data_frame = pd.concat(to_concat, join='outer', axis=1).fillna(0)
        
        if data_frame.values.ndim < 2:
            for i in xrange(data_frame.values.shape[0]):
                row = data_frame.values[i]
                values.append((row > 0).sum())
        else:
            row = data_frame.values
            values.append((row > 0).sum())

    values = np.asarray(values, dtype='i')
    fpath = os.path.join(PLOTS_FOLDER, table_name + '-userqueue-unique.pdf')
    three_plots(values, r'Number of daily objects', fpath, discrete=True)

if __name__ == '__main__':
    plac.call(main)
