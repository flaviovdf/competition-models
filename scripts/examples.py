#-*- coding: utf8
from __future__ import division, print_function

import matplotlib
matplotlib.use('Agg')

from collections import defaultdict
from collections import OrderedDict

from code import db
from code import plot_helper

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon

from scipy import stats

import datetime as dt
import pandas as pd
import seaborn as sns
import numpy as np

MAX = 6 * 60

class Box(object):
    def __init__(self, ypoints, name='', fillcolor='b', edgecolor='k', wstyle='k-'):
        self.ypoints = ypoints
        self.name = name
        self.fillcolor = fillcolor
        self.edgecolor = edgecolor
        self.wstyle = wstyle

def box_plot(boxes):
    mat = []
    labels = []
    for b in boxes:
        mat.append(b.ypoints)
        labels.append(b.name)
    
    n_boxes = len(boxes)

    bp = plt.boxplot(mat, sym='', whis=0)
    ax = plt.gca()
    
    plt.setp(ax, 'xticklabels', [b.name for b in boxes])

    #set colors
    for i in xrange(n_boxes):
        box = bp['boxes'][i]

        box_x = []
        box_y = []
        for j in xrange(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = zip(box_x, box_y)

        box_polygon = Polygon(box_coords, facecolor=boxes[i].fillcolor)
        ax.add_patch(box_polygon)

        plt.setp(box, color=boxes[i].edgecolor)

        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        median_x = []
        median_y = []
        for j in xrange(2):
            median_x.append(med.get_xdata()[j])
            median_y.append(med.get_ydata()[j])
            plt.plot(median_x, median_y, boxes[i].edgecolor)

        dat = boxes[i].ypoints
        perc9   = stats.scoreatpercentile(dat, 9)
        perc25  = stats.scoreatpercentile(dat, 25)
        perc50  = stats.scoreatpercentile(dat, 50)
        perc75  = stats.scoreatpercentile(dat, 75)
        perc91  = stats.scoreatpercentile(dat, 91)
        
        if i % 2 == 1:
            datm1 = boxes[i - 1].ypoints
            perc25m1  = stats.scoreatpercentile(datm1, 25)
            perc50m1  = stats.scoreatpercentile(datm1, 50)
            perc75m1  = stats.scoreatpercentile(datm1, 75)

            plt.quiver(i, perc25m1, \
                1, \
                perc25 - perc25m1, angles='xy', color='k', \
                scale_units='xy', scale=1, width=.004, zorder=999)
            
            plt.quiver(i, perc50m1, \
                1, \
                perc50 - perc50m1, angles='xy', color='k', \
                scale_units='xy', scale=1, width=.004, zorder=999)
            
            plt.quiver(i, perc75m1, \
                1, \
                perc75 - perc75m1, angles='xy', color='k', \
                scale_units='xy', scale=1, width=.004, zorder=999)
        

        tick = i + 1
        mean = np.mean(dat)
        if tick == 1:
            plt.plot([tick], [perc91], 'ko', linewidth=3, markersize=4, \
                    label='$91^{th}$ Percentile')
            plt.plot([tick], [mean], 'Dk', linewidth=3, markersize=4, \
                    label='$Mean$')
            plt.plot([tick], [perc9], 'ks', linewidth=3, markersize=4, \
                    label='$9^{th}$ Percentile')
        else:
            plt.plot([tick], [perc9], 'ks', linewidth=3, markersize=4)
            plt.plot([tick], [perc91], 'ko', linewidth=3, markersize=4)
            plt.plot([tick], [mean], 'Dk', linewidth=3, markersize=4)
        

        plt.plot([tick, tick], [perc9, perc25], 'k-')
        plt.plot([tick, tick], [perc75, perc91], 'k-')

def get_deltas(trace, obj_interest, complement=False):

    deltas = OrderedDict()
    prev_date = None
    curr_attention = None

    for tstamp, user, obj in trace:
         
        if user not in deltas:
            deltas[user] = 0

        date = dt.date.fromtimestamp(tstamp)
        if prev_date is None or prev_date != date:
            prev_date = date
            prev_seen = {}

            if curr_attention is not None:
                for seen_user in curr_attention:
                    deltas[seen_user] += curr_attention[seen_user]

            curr_attention = defaultdict(int)

        if user in prev_seen:
            curr_attention[user] += min(MAX, tstamp - prev_seen[user])
        
        if (not complement and obj == obj_interest) or \
                (complement and obj != obj_interest):
            prev_seen[user] = tstamp
        else:
            if user in prev_seen:
                del prev_seen[user]
    
    return deltas

def get_before_after(attention_others, attention_obj, users_to_consider):

    values_obj = []
    values_others = []
                
    for user in users_to_consider:
        values_obj.append(attention_obj[user])
        values_others.append(attention_others[user])
                                            
    return np.asarray(values_obj), np.asarray(values_others)

def bplot(before, after, obj, obj_name):
    
    attention_others_before = get_deltas(before, obj, True)
    attention_others_after = get_deltas(after, obj, True)
    
    attention_obj_before = get_deltas(before, obj, False)
    attention_obj_after = get_deltas(after, obj, False)

    users_of_interest = sorted([user \
            for user in attention_obj_before \
            if attention_obj_before[user] and \
            user in attention_obj_after and attention_obj_after[user]])
    
    from_values_obj, from_values_others = \
            get_before_after(attention_others_before, attention_obj_before, \
            users_of_interest)

    to_values_obj, to_values_others = \
            get_before_after(attention_others_after, attention_obj_after, \
            users_of_interest)

    boxes = [
             Box(from_values_obj, \
                     name='Artist \n Before Release', \
                     fillcolor='lightgreen'),

             Box(to_values_obj, \
                     name='Artist \n After Release', \
                     fillcolor='pink'),

             Box(from_values_others, \
                     name='Others \n Before Release', \
                     fillcolor='lightgreen'),

             Box(to_values_others, \
                     name='Others \n After Release', \
                     fillcolor='pink')
             ]
    
    sns.set_style('white')
    box_plot(boxes)
    plt.ylabel('Total Attention per Artist (Seconds in 60 days window)')
    ax = plt.gca()
    ax.set_ylim((1e2, 1e7))
    ax.set_yscale('log')
    plt.legend(loc='best')
    plt.savefig('before_after_bplot_' + obj_name + '.pdf')
    plt.close()

def main():
    plot_helper.initialize_matplotlib()

    releases = {
            'Radiohead':1191974400,
            'Coldplay':1213228800,
            'Rihanna':1180573069,
            'Britney Spears':1227833869
            }

    for obj_name in releases:
        id2name, name2id = db.get_mappings('lastfm_artist')
        before, after = db.filter_release('lastfm_artist', releases[obj_name])
    
        bplot(before, after, name2id[obj_name], obj_name)

if __name__ == '__main__':
    main()
