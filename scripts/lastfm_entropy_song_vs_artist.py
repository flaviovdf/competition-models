#!/usr/bin/env python
# -*- coding: utf8

from __future__ import division, print_function

from code import config
from code import db

from collections import defaultdict

from matplotlib import pyplot as plt
from matplotlib import rc

import numpy as np
import os
import plac

def initialize_matplotlib(): 
    inches_per_pt = 1.0 / 72.27 
    golden_mean = (np.sqrt(5) - 1.0) / 2.0 
    
    fig_width = 2 * 240.0 * inches_per_pt
    #fig_height = .25 * fig_width
    fig_height = fig_width

    rc('axes', labelsize=8) 
    rc('axes', titlesize=7) 
    rc('axes', unicode_minus=False) 
    rc('axes', grid=False) 
    rc('figure', figsize=(fig_width, fig_height)) 
    rc('grid', linestyle=':') 
    rc('font', family='serif') 
    rc('legend', fontsize=8) 
    rc('lines', linewidth=1) 
    rc('ps', usedistiller='xpdf') 
    rc('text', usetex=True) 
    rc('xtick', labelsize=7) 
    rc('ytick', labelsize=7)
    rc('xtick', direction='out') 
    rc('ytick', direction='out')

def zf_entropy(n):
    r = np.arange(n) + 1
    r = r * np.log(1.78 * n)
    p = 1 / r
    p /= p.sum()

    return (-np.log2(p) * p).sum()

def entropy(data):
    data = np.asarray(data)
    p = data / data.sum()
    return (-np.log2(p) * p).sum()

def main():
   
    initialize_matplotlib()

    users_artist_count = defaultdict(lambda: defaultdict(int))
    users_song_count = defaultdict(lambda: defaultdict(int))

    ids2name_artist_db, _ = db.get_mappings('lastfm_artist')
    ids2name_song_db, _ = db.get_mappings('lastfm_song')
    
    for _, user, obj in db.iter_sorted('lastfm_artist'):
        users_artist_count[ids2name_song_db[user]][obj] += 1
    
    for _, user, obj in db.iter_sorted('lastfm_song'):
        users_song_count[ids2name_song_db[user]][obj] += 1
    
    x_h = []
    y_h = []
    
    x_p = []
    y_p = []

    for user in users_artist_count:
        plays_artists = users_artist_count[user]

        if user in users_song_count:
            plays_songs = users_song_count[user]
            
            x_h.append(entropy(plays_artists.values()))
            y_h.append(entropy(plays_songs.values()))
            
            x_p.append(len(plays_artists))
            y_p.append(len(plays_songs))

    out_folder = config.PLOTS_FOLDER

    fname = os.path.join(out_folder, 'lastfm-entropy-artist-vs-song.pdf')
    plt.plot(x_h, y_h, 'wo')
    plt.xlabel('Entropy Artists')
    plt.ylabel('Entropy Songs')
    plt.savefig(fname)
    plt.close()

    fname = os.path.join(out_folder, 'lastfm-plays-artist-vs-song.pdf')
    plt.loglog(x_p, y_p, 'wo')
    plt.xlabel('Number of Artists')
    plt.ylabel('Number of Songs')
    plt.savefig(fname)
    plt.close()

    fname = os.path.join(out_folder, 'lastfm-plays-artist-vs-entropy.pdf')
    plt.semilogx(x_p, x_h, 'wo')
    plt.semilogx(x_p, [entropy(np.ones(x)) for x in x_p], 'k-', \
            label='Uniform')
    plt.semilogx(np.unique(x_p), [zf_entropy(x) for x in np.unique(x_p)], 'b--', \
            label='ZipF')
    plt.xlabel('Number of Artists')
    plt.ylabel('Entropy Artists')
    plt.legend()
    plt.savefig(fname)
    plt.close()
    
    fname = os.path.join(out_folder, 'lastfm-plays-songs-vs-entropy.pdf')
    plt.semilogx(y_p, y_h, 'wo')
    plt.semilogx(x_p, [entropy(np.ones(x)) for x in x_p], 'k-', \
            label='Uniform')
    plt.semilogx(np.unique(x_p), [zf_entropy(x) for x in np.unique(x_p)], 'b--', \
            label='ZipF')
    plt.xlabel('Number of Songs')
    plt.ylabel('Entropy Songs')
    plt.legend()
    plt.savefig(fname)
    plt.close()

if __name__ == '__main__':
    plac.call(main)
