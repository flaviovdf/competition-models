#-*- coding: utf8
from __future__ import division, print_function

from code import config
from code import db

from collections import defaultdict

import numpy as np
import os
import pandas as pd
import plac

def main():
    
    for table_name in config.TABLES:
        obj_tstamps = defaultdict(list)
        for tstamp, user, obj in db.iter_sorted(table_name):
            obj_tstamps[obj].append(tstamp)
        
        fpath = os.path.join(config.TSERIES_FOLDER, table_name + '.h5')
        store = pd.HDFStore(fpath)
        for obj in obj_tstamps:
            obj_ticks = obj_tstamps[obj]
            if len(obj_ticks) < 500:
                continue

            date_index = pd.to_datetime(obj_ticks, unit='s')
            tseries = pd.Series(np.ones(len(date_index)), index=date_index)
            store['_' + str(obj)] = tseries

        store.close()

if __name__ == '__main__':
    plac.call(main)
