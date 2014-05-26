#-*- coding: utf8
'''
Plots the inter-arrival time for objects
'''
from __future__ import division, print_function

from code import db
from code.config import TABLES
from code.config import PLOTS_FOLDER

from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib import pyplot as plt
from scipy import stats as ss

import os
import numpy as np
import plac
import powerlaw

def main(table_name):
    if table_name not in TABLES:
        raise Exception('Choose table_name from: ' + ' '.join(TABLES))

    seen = {}
    deltas = []

    for tstamp, user, obj in db.iter_sorted(table_name):
        if obj in seen:
            delta = tstamp - seen[obj]
            if delta != 0:
                deltas.append(delta)
        seen[obj] = tstamp
   
    deltas = np.asarray(deltas)
    np.random.shuffle(deltas)

    ecdf = ECDF(deltas)
    x = np.linspace(deltas.min(), deltas.max(), 2000)

    #params = ss.expon.fit(deltas)
    #fit_ccdf = 1 - ss.expon.cdf(x, loc=params[0], scale=params[1])
    
    #deltas_copy = deltas.copy()
    #np.random.shuffle(deltas_copy)

    fit = powerlaw.Fit(deltas, xmin=deltas.min())

    fig = plt.figure(figsize=(12, 4))
   
    #plt.subplot(131)
    #plt.plot(x, y, 'wo')
    #plt.xlabel(r'$\delta$ between plays for user, obj')
    #plt.ylabel('Count')
    
    plt.subplot(121)
    plt.loglog(x, ecdf(x), 'k-')
    ax = plt.gca()
 
    #fit.exponential.plot_cdf(ax=ax, color='blue', label='Exp')
    #fit.power_law.plot_cdf(ax=ax, color='red', label='Plaw')
    #fit.truncated_power_law.plot_cdf(ax=ax, color='green', label='Plaw + exp cut')
    #fit.stretched_exponential.plot_cdf(ax=ax, color='cyan', label='Streched expon')
    
    plt.legend(loc='lower right')

    plt.xlabel(r'$\delta$ between access for obj')
    plt.ylabel('CDF')
   
    plt.subplot(122)
    plt.loglog(x, 1 - ecdf(x), 'k-')
    ax = plt.gca()
    
    #fit.exponential.plot_ccdf(ax=ax, color='blue', label='Exp')
    #fit.power_law.plot_ccdf(ax=ax, color='red', label='Plaw')
    #fit.truncated_power_law.plot_ccdf(ax=ax, color='green', label='Plaw + exp cut')
    #fit.stretched_exponential.plot_ccdf(ax=ax, color='cyan', label='Streched expon')

    plt.legend(loc='lower left')

    #plt.semilogy(x, fit_ccdf, 'b--')
    plt.xlabel(r'$\delta$ between access for user, obj')
    plt.ylabel('CCDF')
    
    plt.tight_layout(pad=0)
    fpath = os.path.join(PLOTS_FOLDER, table_name + '_obj_inter_arrival.pdf')
    plt.savefig(fpath)
    plt.close()

if __name__ == '__main__':
    plac.call(main)
