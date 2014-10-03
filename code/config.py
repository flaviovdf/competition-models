#-*- coding: utf8
'''
Configuration properties such as file paths
'''
from __future__ import division, print_function

import os

#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = '/home/vod/flaviov/workspace/competition'
relative_fpath_opt = lambda fpath: os.path.join(BASE_DIR, fpath)

#DB config
DB_FOLDER = relative_fpath_opt('db')
DB_FPATH = relative_fpath_opt(os.path.join('db', 'triples.h5'))

LASTFM_ARTIST_TABLE = 'lastfm_artist'
LASTFM_SONG_TABLE = 'lastfm_song'

LASTFM_OUR_ARTIST_TABLE = 'lastfm_our_artist'
LASTFM_OUR_SONG_TABLE = 'lastfm_our_song'

TWITTER_MOVIE_TABLE = 'twitter_movie'
TWITTER_GENRE_TABLE = 'twitter_genre'

YOUTUBE_UFMG_TABLE = 'youtube_ufmg'

BRIGHTKITE_TABLE = 'brightkite_locs'

TWITTER_HASHTAG_TABLE = 'twitter_hashtag'

TWITTER_MMUSIC_ARTIST_TABLE = 'mmusic_artist'
TWITTER_MMUSIC_SONG_TABLE = 'mmusic_song'

TABLES = (LASTFM_ARTIST_TABLE, LASTFM_SONG_TABLE, \
        LASTFM_OUR_ARTIST_TABLE, LASTFM_OUR_SONG_TABLE, \
        TWITTER_MOVIE_TABLE, TWITTER_GENRE_TABLE, \
        YOUTUBE_UFMG_TABLE, BRIGHTKITE_TABLE, \
        TWITTER_HASHTAG_TABLE, TWITTER_MMUSIC_ARTIST_TABLE, \
        TWITTER_MMUSIC_SONG_TABLE)

#DB key to name mappings files
LASTFM_SONG_NAMES = relative_fpath_opt(os.path.join('db', 'lastfm_song.ids'))
LASTFM_ARTIST_NAMES = relative_fpath_opt(os.path.join('db', \
        'lastfm_artist.ids'))

LASTFM_OUR_SONG_NAMES = relative_fpath_opt(os.path.join('db', \
        'lastfm_our_song.ids'))
LASTFM_OUR_ARTIST_NAMES = relative_fpath_opt(os.path.join('db', \
        'lastfm_our_artist.ids'))

TWITTER_MOVIE_NAMES = relative_fpath_opt(os.path.join('db', \
        'twitter_movie.ids'))
TWITTER_GENRES_NAMES = relative_fpath_opt(os.path.join('db', \
        'twitter_genre.ids'))

YOUTUBE_UFMG_NAMES = relative_fpath_opt(os.path.join('db', \
        'youtube_ufmg.ids'))

BRIGHTKITE_NAMES = relative_fpath_opt(os.path.join('db', \
        'brightkite_loc.ids'))

TWITTER_HASHTAG_NAMES = relative_fpath_opt(os.path.join('db', \
        'twitter_hashtag.ids'))

TWITTER_MMUSIC_ARTIST_NAMES = relative_fpath_opt(os.path.join('db', \
        'mmusic_artist.ids'))
TWITTER_MMUSIC_SONG_NAMES = relative_fpath_opt(os.path.join('db', \
        'mmusic_song.ids'))

#Tseries folder
TSERIES_FOLDER = relative_fpath_opt('tseries')

#Where we keep the raw datasets
RAW_DATA_FPATH = relative_fpath_opt('raw_data')

#LastFM data
LASTFM_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, 'lastfm'))
LASTFM_ORIGINAL = os.path.join(LASTFM_FOLDER, \
        'userid-timestamp-artid-artname-traid-traname.tsv')

LASTFM_OUR_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, 'our_lfm'))
LASTFM_OUR_ORIGINAL = os.path.join(LASTFM_OUR_FOLDER, 'our_trace.dat')

#Movies data
MOVIE_TWEETS_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'movie_tweets'))
MOVIE_TWEETS_ORIGINAL = os.path.join(MOVIE_TWEETS_FOLDER, 'ratings.dat')
MOVIE_INFO_ORIGINAL = os.path.join(MOVIE_TWEETS_FOLDER, 'movies.dat')

#Youtube UFMG original
YOUTUBE_UFMG_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'youtube_ufmg'))
YOUTUBE_UFMG_ORIGINAL = os.path.join(YOUTUBE_UFMG_FOLDER, 'video_trace.txt')

#Brightkite data
BRIGHTKITE_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'brightkite'))
BRIGHTKITE_ORIGINAL = os.path.join(BRIGHTKITE_FOLDER, \
        'loc-brightkite_totalCheckins.txt')

#Movies data
MOVIE_TWEETS_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'movie_tweets'))
MOVIE_TWEETS_ORIGINAL = os.path.join(MOVIE_TWEETS_FOLDER, 'ratings.dat')
MOVIE_INFO_ORIGINAL = os.path.join(MOVIE_TWEETS_FOLDER, 'movies.dat')

#Youtube UFMG original
YOUTUBE_UFMG_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'youtube_ufmg'))
YOUTUBE_UFMG_ORIGINAL = os.path.join(YOUTUBE_UFMG_FOLDER, 'video_trace.txt')

#Brightkite data
BRIGHTKITE_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'brightkite'))
BRIGHTKITE_ORIGINAL = os.path.join(BRIGHTKITE_FOLDER, \
        'loc-brightkite_totalCheckins.txt')

#Hashtags data
TWITTER_HASHTAG_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'hashtags'))
TWITTER_HASHTAG_ORIGINAL = os.path.join(TWITTER_HASHTAG_FOLDER, 'hashtags.txt')

#MMusic data
TWITTER_MMUSIC_FOLDER = relative_fpath_opt(os.path.join(RAW_DATA_FPATH, \
        'mmusic'))
TWITTER_MMUSIC_ORIGINAL = os.path.join(TWITTER_MMUSIC_FOLDER, 'tweet.txt')
TWITTER_MMUSIC_ARTIST_FILE = os.path.join(TWITTER_MMUSIC_FOLDER, 'artists.txt')
TWITTER_MMUSIC_SONG_FILE = os.path.join(TWITTER_MMUSIC_FOLDER, 'track.txt')

#Plots
PLOTS_FOLDER = relative_fpath_opt('plots')
