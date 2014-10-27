#-*- coding: utf8
from __future__ import division, print_function

from collections import defaultdict
from code import db

import datetime as dt
import numpy as np
import plac

def count_plays(table, valid):
    
    counts = defaultdict(int)
    for _, user, obj in table:
        if obj in valid:
            counts[user] += 1
    
    return counts

def main(table_name):
    releases = {
            'Radiohead':1191974400,
            'Coldplay':1213228800,
            'Rihanna':1180573069,
            'Britney Spears':1227833869
            }

    id2name, name2id = db.get_mappings(table_name)

    for artist, release_date in releases.items():
        before_after = db.filter_release(table_name, release_date)

        user_plays_before_fpath = open(\
                artist +'_lta_user_plays_before.dat', 'w')
        user_plays_after_fpath = open(\
                artist + '_lta_user_plays_after.dat', 'w')
        
        transitions_before_fpath = open(\
                artist + '_lta_transitions_before.dat', 'w')
        transitions_after_fpath = open(\
                artist + '_lta_transitions_after.dat', 'w')
        
        lta_ids_before_fpath = open(\
                artist + '_lta_ids_before.dat', 'w')
        lta_ids_after_fpath = open(\
                artist + '_lta_ids_after.dat', 'w')
        
        dbefore = open(artist + '_deltas_before_release.dat', 'r')
        dafter = open(artist + '_deltas_after_release.dat', 'r')

        ubefore_after = [user_plays_before_fpath, user_plays_after_fpath]
        tbefore_after = [transitions_before_fpath, transitions_after_fpath]
        idsfiles = [lta_ids_before_fpath, lta_ids_after_fpath]
        dfiles = [dbefore, dafter]

        for i in [0, 1]:
            table = before_after[i]
            
            u = ubefore_after[i]
            t = tbefore_after[i]
            d = dfiles[i]
            id_f = idsfiles[i]

            d.readline()
            valid_objs = set()
            ids = {}
            for line in d:
                spl = line.split('\t')
                valid_objs.add(name2id[spl[0]])
                ids[spl[0]] = len(ids) + 1

            counts = count_plays(table, valid_objs)
            for user in counts:
                print(counts[user], end='\t', file=u)

            for _, user, obj in table:
                if obj in valid_objs:
                    print(ids[id2name[obj]], end='\t', file=t)
            
            for obj in ids:
                print(obj, ids[obj], sep='\t', file=id_f)

            d.close()
            u.close()
            t.close()
            id_f.close()

if __name__ == '__main__':
    plac.call(main)
