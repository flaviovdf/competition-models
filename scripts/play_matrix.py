#-*- coding: utf8
from __future__ import division, print_function

from collections import defaultdict

from code import db

import plac

def main(table_name):

    id2name, name2id = db.get_mappings(table_name)
    plays = defaultdict(int)
    for tstamp, user, obj in db.iter_sorted(table_name):
        plays[user, obj] += 1

    for user, obj in sorted(plays):
        print(user, id2name[obj], plays[user, obj], sep='\t')

if __name__ == '__main__':
    plac.call(main)
