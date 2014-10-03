#-*- coding: utf8
from __future__ import division, print_function

from code import db
from code.config import PLOTS_FOLDER
from code.plot_helper import initialize_matplotlib
from code.plot_helper import three_plots

import os
import numpy as np
import plac

def resample(user_tseries):
    rv = {}
    for user in user_tseries:
        rv[user] = user_tseries[user].resample('1d', how='sum', \
                closed='left').fillna(0)
    return rv

def main(table_name):
    
    initialize_matplotlib()

    user_tseries = db.get_user_timeseries(table_name)
    user_tseries = resample(user_tseries)
    
    values = []
    for user in user_tseries:
        values.extend(user_tseries[user].values)
    
    values = np.asarray(values, dtype='i')
    fpath = os.path.join(PLOTS_FOLDER, table_name + '-userqueue.pdf')
    three_plots(values, r'Number of daily visits', fpath, discrete=True)

if __name__ == '__main__':
    plac.call(main)
