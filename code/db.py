#-*- coding: utf8
from __future__ import division, print_function

from .config import DB_FOLDER 
from .config import DB_FPATH

import numpy as np
import os
import pandas as pd
import tables

NANO = 10 ** 9

def _to_pandas(time_stamps):
    time_series = {}
    for key in time_stamps:
        ticks = np.asarray(time_stamps[key])
        index = pd.DatetimeIndex(ticks * NANO)
        time_series[key] = pd.Series(np.ones(ticks.shape[0]), index=index)
    return time_series

def my_grep(name2ids, text):
    '''
    A poor man's grep to find ids with a given string as name

    Parameters
    ----------
    names2ids : dict
        the names 2 ids mappings
    text : str
        text to grep
    '''
    keys = name2ids.keys()
    rv = {}
    for key in keys:
        if text.lower() in key.lower():
            rv[key] = name2ids[key]
    return rv

def get_mappings(table_name):
    '''
    Returns two dictionaries, one for the mappings
    of id > name, the other with name -> id.

    Parameters
    ----------
    table_name : str
        the table to iterate
    '''
    fpath = os.path.join(DB_FOLDER, table_name + '.ids')
    ids2name = {}
    name2ids = {}
    with open(fpath) as ids_file:
        for line in ids_file:
            spl = line.split('\t')
            
            id_ = int(spl[0])
            if len(spl) > 1:
                name = spl[1].strip()
            else:
                name = ''

            ids2name[id_] = name
            name2ids[name] = id_

    return ids2name, name2ids

def get_user_obj_timeseries(table_name):
    '''
    Returns a dictionary with the time series from
    a user to a object. The key is a tuple (user, obj)

    Parameters
    ----------
    table_name : str
        the table to iterate
    '''
    time_stamps = {}
    for tstamp, user, obj in iter_sorted(table_name):
        if (user, obj) not in time_stamps:
            time_stamps[user, obj] = []

        time_stamps[user, obj].append(tstamp)

    return _to_pandas(time_stamps)

def get_obj_timeseries(table_name):
    '''
    Returns a dictionary with the time series for
    an object.

    Parameters
    ----------
    table_name : str
        the table to iterate
    '''

    time_stamps = {}
    for tstamp, user, obj in iter_sorted(table_name):
        if obj not in time_stamps:
            time_stamps[obj] = []

        time_stamps[obj].append(tstamp)

    return _to_pandas(time_stamps)

def get_user_timeseries(table_name):
    '''
    Returns a dictionary with the time series for
    an user.

    Parameters
    ----------
    table_name : str
        the table to iterate
    '''

    time_stamps = {}
    for tstamp, user, obj in iter_sorted(table_name):
        if user not in time_stamps:
            time_stamps[user] = []

        time_stamps[user].append(tstamp)

    return _to_pandas(time_stamps)

def filter_release(table_name, release_date, delta_str='60D'):
    '''
    Filters a database before and after a given date
    
    Parameters
    ----------
    table_name : str
        the table to filter
    release_date : int
        the date to filter before and after (seconds from epoch)
    delta_str: str
        the delta before and after to filter (e.g., 60D)
    '''

    delta = float(pd.to_timedelta(delta_str) / 1e9)
    
    before_start = release_date - delta
    after_end = release_date + delta
    
    query = '(date > %f) & (date <= %f)'
    
    before = query % (before_start, release_date)
    after = query % (release_date, after_end)
    
    before_release = [x for x in iter_sorted(table_name, before)]
    after_release = [x for x in iter_sorted(table_name, after)]
    
    return before_release, after_release

def iter_sorted(table_name, where=None):
    '''
    Returns a generator that iters through the table sorted
    by date

    Parameters
    ----------
    table_name : str
        the table to iterate
    where : str
        query condition
    '''
    with tables.open_file(DB_FPATH, 'r') as tables_file:
        table = tables_file.get_node('/', table_name)
        
        if where:
            rows = table.where(where)
        else:
            rows = table.itersorted('date')

        last_seen = {}
        for row in rows:
            tstamp = row['date']
            user = row['user_id']
            obj = row['object_id']
            
            if (user, obj) in last_seen and last_seen[user, obj] == tstamp:
                continue
            
            last_seen[(user, obj)] = tstamp
            yield tstamp, user, obj
