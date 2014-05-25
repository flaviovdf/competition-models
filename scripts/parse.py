#!/usr/bin/env python
#-*- coding: utf8
from __future__ import division, print_function
'''
Parsers datafiles to h5 db
'''
from code import config
from code import parser 

import os
import plac

def main():
    h5_file = config.DB_FPATH

    parser.convert(parser.movies_iter_triples(), h5_file, \
            config.TWITTER_MOVIE_TABLE, config.TWITTER_MOVIE_NAMES, \
            mode='w')
    parser.convert(parser.movies_iter_triples(True), h5_file, \
            config.TWITTER_GENRE_TABLE, config.TWITTER_GENRES_NAMES)

    parser.convert(parser.lfm_iter_triples(), h5_file, \
            config.LASTFM_ARTIST_TABLE, config.LASTFM_ARTIST_NAMES)
    parser.convert(parser.lfm_iter_triples(True), h5_file, \
            config.LASTFM_SONG_TABLE, config.LASTFM_SONG_NAMES)

if __name__ == '__main__':
    plac.call(main)
