#-*- coding: utf8
from __future__ import division, print_function

from .config import DB_FPATH 

import tables

def iter_sorted(table_name):
    '''
    Returns a generator that iters through the table sorted
    by date

    Parameters
    ----------
    table_name : str
        the table to iterate
    '''
    with tables.open_file(DB_FPATH, 'r') as tables_file:
        table = tables_file.get_node('/', table_name)

        for row in table.itersorted('date'):
            tstamp = row['date']
            user = row['user_id']
            obj = row['object_id']

            yield tstamp, user, obj
