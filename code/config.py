#-*- coding: utf8
'''
Configuration properties such as file paths
'''
from __future__ import division, print_function

import os

#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = '/Users/flaviov/workspace/competition'
relative_fpath_opt = lambda fpath: os.path.join(BASE_DIR, fpath)

#DB config
DB_FOLDER = relative_fpath_opt('db')
DB_FPATH = relative_fpath_opt(os.path.join('db', 'triples.h5'))

LASTFM_ARTIST_TABLE = 'lastfm_artist'
LASTFM_SONG_TABLE = 'lastfm_songs'

TWITTER_MOVIE_TABLE = 'twitter_movie'
TWITTER_GENRE_TABLE = 'twitter_genre'

#DB key to name mappings files
LASTFM_SONG_NAMES = relative_fpath_opt(os.path.join('db', 'lastfm_songs.ids'))
LASTFM_ARTIST_NAMES = relative_fpath_opt(os.path.join('db', \
        'lastfm_artist.ids'))

TWITTER_MOVIE_NAMES = relative_fpath_opt(os.path.join('db', \
        'twitter_movie.ids'))
TWITTER_GENRES_NAMES = relative_fpath_opt(os.path.join('db', \
        'twitter_genre.ids'))

TABLES = (LASTFM_ARTIST_TABLE, LASTFM_SONG_TABLE, \
        TWITTER_MOVIE_TABLE, TWITTER_GENRE_TABLE)

#Tseries folder
TSERIES_FOLDER = relative_fpath_opt('tseries')

#Where we keep the raw datasets
RAW_DATA_FPATH = relative_fpath_opt('raw_data')

#LastFM data
LASTFM_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, 'lastfm'))
LASTFM_ORIGINAL = os.path.join(LASTFM_FOLDER, \
        'userid-timestamp-artid-artname-traid-traname.tsv')

#Movies data
MOVIE_TWEETS_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'movie_tweets'))
MOVIE_TWEETS_ORIGINAL = os.path.join(MOVIE_TWEETS_FOLDER, 'ratings.dat')
MOVIE_INFO_ORIGINAL = os.path.join(MOVIE_TWEETS_FOLDER, 'movies.dat')

#Plots
PLOTS_FOLDER = relative_fpath_opt('plots')
