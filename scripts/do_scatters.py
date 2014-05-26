#!/usr/bin/env python
from __future__ import division, print_function

from matplotlib import pyplot as plt

import numpy as np
import plac

def main(ids_fpath, rates_fpath, plays_fpath):
    mb_to_name = {}
    name_to_mb = {}

    with open(ids_fpath) as f:
        for line in f:
            spl = line.split()
            mbid = spl[0]
            name = ' '.join(spl[1:])

            mb_to_name[mbid] = name
            name_to_mb[name] = mbid

    rates = {}
    with open(rates_fpath) as f:
        for line in f:
            spl = line.split()
            mbid = spl[0]

            rates[mbid] = np.array([float(x) for x in spl[1:]])

    plays = {}
    with open(plays_fpath) as f:
        for line in f:
            spl = line.split()
            mbid = spl[0]

            plays[mbid] = np.array([float(x) for x in spl[1:]])

    i = 0
    n_bins = 10
    for artist in ['Ladytron', 'Britney Spears', 'Radiohead', \
            'Metallica', 'Daft Punk', 'Yann Tiersen']:
        rate = rates[name_to_mb[artist]]
        play = plays[name_to_mb[artist]]
    
        lifetime = (play / rate)
    
        idx_sorted = play.argsort()
        bin_size = int(idx_sorted.shape[0] / n_bins)
    
        mean_lifetime = []
        mean_plays = []
        for j in range(0, idx_sorted.shape[0], bin_size):
            idx = idx_sorted[j:j + bin_size]
            mean_lifetime.append(lifetime[idx].mean())
            mean_plays.append(play[idx].mean())

        median_lifetime = []
        median_plays = []
        for j in range(0, idx_sorted.shape[0], bin_size):
            idx = idx_sorted[j:j + bin_size]
            median_lifetime.append(np.median(lifetime[idx]))
            median_plays.append(np.median(play[idx]))

        plt.subplot(2, 3, i + 1)
        plt.title(artist)
        plt.semilogy(lifetime, play, 'wo')
        plt.semilogy(mean_lifetime, mean_plays, 'bo')
        plt.semilogy(mean_lifetime, mean_plays, 'b-', label='Mean')
    
        plt.semilogy(median_lifetime, median_plays, 'ro')
        plt.semilogy(median_lifetime, median_plays, 'r-', label='Median')
    
        plt.legend()
        plt.xlabel('Lifetime')
        plt.ylabel('Plays')
    
        i += 1

    plt.tight_layout(pad=0)
    #plt.savefig('time_plays.pdf')
    plt.show()

if __name__ == '__main__':
    plac.call(main)
