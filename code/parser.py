#-*- coding: utf8
from __future__ import division, print_function

from .common import ContiguousID

from .config import MOVIE_TWEETS_ORIGINAL
from .config import MOVIE_INFO_ORIGINAL
from .config import LASTFM_ORIGINAL

import tables
import time
import os

def movies_iter_triples(use_genre=False):
    '''
    Iterates over the movies dataset file and returns a generator.
    Each row in the generator is: (timestamp, user, content, content_name)

    Parameters
    ----------
    use_genre : bool (defaults to False)
        If True, content will be the movie genre and not the movie id.
    '''
    
    genres = {}
    names = {}
    with open(MOVIE_INFO_ORIGINAL) as info_file:
        for line in info_file:
            spl = line.split('::')
            movie_id, movie_name, genres_str = spl
            genres[movie_id] = set(x.strip() for x in genres_str.split('|'))
            names[movie_id] = movie_name

    with open(MOVIE_TWEETS_ORIGINAL) as tripes_file:
        for line in tripes_file:
            spl = line.split('::')
            user_id, movie_id, rating, rating_timestamp = spl
            rating_timestamp = float(rating_timestamp)

            if use_genre:
                for genre_name in genres[movie_id]:
                    yield rating_timestamp, user_id, genre_name, genre_name
            else:
                yield rating_timestamp, user_id, movie_id, names[movie_id]

def lfm_iter_triples(use_songs=False):
    '''
    Iterates over the lastfm dataset file and returns a generator.
    Each row in the generator is: (timestamp, user, content, content_name)

    Parameters
    ----------
    use_songs : bool (defaults to False)
        If True, content will be songs. If False, content will be artists.
    '''

    with open(LASTFM_ORIGINAL) as triples_file:
        for line in triples_file:
            spl = line.split('\t')
            
            user = spl[0]
            tstamp = spl[1]
            artist = spl[2]
            artist_name = spl[3]
            song = spl[4]
            song_name = spl[5]

            tstamp_split = tstamp.split('T')
            tstamp_day = tstamp_split[0]
            tstamp_hour = tstamp_split[1][:-1]
            
            tstamp_string = '%s %s' % (tstamp_day, tstamp_hour)
            tstamp_seconds = time.mktime(\
                    time.strptime(tstamp_string, '%Y-%m-%d %H:%M:%S'))

            if use_songs:
                content = song
                content_name = song_name
            else:
                content = artist
                content_name = artist_name
            
            if content.strip():
                yield tstamp_seconds, user, content, content_name

class UserObject(tables.IsDescription):
    user_id = tables.Int32Col()
    object_id = tables.Int32Col()
    date = tables.Float32Col()

def convert(date_user_obj_name, table_fpath, table_name, ids_fpath, mode='a'):
    '''
    Convert's triple to a h5 database

    Parameters
    ----------
    date_user_obj_name : iterable
        yield a date (in seconds), user, object and object_name tuple
    table_fpath : str
        path of the h5 file
    table_name : str
        the name of the table to save
    ids_fpath : str
        where to save id -> name mappings
    '''
    user_ids = ContiguousID()
    object_ids = ContiguousID()
    names = {}

    h5_file = tables.open_file(table_fpath, mode)
    table = h5_file.create_table('/', table_name, UserObject)
    
    for date, user, obj, obj_name in date_user_obj_name:
        row = table.row

        user_id = user_ids[user]
        object_id = object_ids[obj]
        names[object_id] = obj_name

        row['user_id'] = user_id
        row['object_id'] = object_id
        row['date'] = date
        row.append()
    
    table.flush()
    table.cols.date.create_csindex()
    h5_file.close()

    with open(ids_fpath, 'w') as ids_file:
        for key in names:
            print(key, names[key].strip(), sep='\t', file=ids_file)
