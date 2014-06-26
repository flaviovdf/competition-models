#-*- coding: utf8

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from matplotlib import rc

from statsmodels.distributions.empirical_distribution import ECDF

import numpy as np
import powerlaw

def initialize_matplotlib(): 
    inches_per_pt = 1.0 / 72.27 
    golden_mean = (np.sqrt(5) - 1.0) / 2.0 
    
    fig_width = 2 * 240.0 * inches_per_pt
    fig_height = .25 * fig_width

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

def three_plots(data, xlabel, fpath, discrete=True, xmin=None):
    
    data = np.asanyarray(data)
    data = data[data > 0]
    
    if xmin is None:
        fit = powerlaw.Fit(data, discrete=discrete, xmin=data.min())
    else:
        fit = powerlaw.Fit(data, discrete=discrete, xmin=xmin)

    ecdf = ECDF(data)

    n = data.shape[0]
    
    log_min_size = np.log10(data.min())
    log_max_size = np.log10(data.max())
    nbins = np.ceil((log_max_size - log_min_size) * min(n, 10))
    bins = np.unique(np.floor(np.logspace(log_min_size, log_max_size, nbins)))
    
    hist, edges = np.histogram(data, bins)
    x = (edges[1:] + edges[:-1]) / 2.0
    
    if not x.any():
        return

    plt.subplot(131)
    plt.ylabel(r'Number of occurences', labelpad=0)
    plt.xlabel(xlabel, labelpad=0)
    
    if discrete:
        counts = np.bincount(data)
        xvals = np.arange(counts.shape[0]) + 1
        plt.loglog(xvals, counts, 'wo', ms=3)
    else:
        plt.loglog(x, hist, 'wo', ms=3)

    plt.subplot(132)
    plt.xlabel(xlabel, labelpad=0)
    plt.ylabel(r'$P(X > x)$', labelpad=0)
    plt.loglog(x, 1 - ecdf(x), 'wo', ms=3, \
            label='data')
    fit.power_law.plot_ccdf(ax=plt.gca(), color='g', linestyle='-.', \
            label='PLaw(%.2f)' % fit.power_law.alpha)
    fit.lognormal.plot_ccdf(ax=plt.gca(), color='b', linestyle='--', \
            label='Ln N(%.2f, %.2f)' % (fit.lognormal.parameter1, fit.lognormal.parameter2))
    plt.legend(loc='lower left', frameon=False)
    
    plt.subplot(133)
    plt.xlabel(xlabel, labelpad=0)
    plt.ylabel(r'Odds Ratio', labelpad=0)

    odds_ratio = ecdf(x) / (1 - ecdf(x))
    odds_plaw = fit.power_law.cdf(x) / fit.power_law.ccdf(x) 
    odds_lognorm = fit.lognormal.cdf(x) / fit.lognormal.ccdf(x)
    
    plt.loglog(x, odds_ratio, 'wo', ms=3)
    plt.loglog(x[x > fit.xmin], odds_plaw, 'g-')
    plt.loglog(x[x > fit.xmin], odds_lognorm, 'b--')
    
    plt.tight_layout(pad=1)
    plt.savefig(fpath)
    plt.close()
