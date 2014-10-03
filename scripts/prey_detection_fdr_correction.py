#-*- coding: utf8
from __future__ import division, print_function

from statsmodels.stats import multitest

import numpy as np
import plac

def main(table_fpath, fdr=.1):
   
    pvalues = []
    with open(table_fpath) as tables_file:
        for line in tables_file:
            if '#' in line:
                continue
            spl = line.split('\t')
            if len(spl) == 5:
                pvalues.extend(float(x) for x in spl[1:])
    
    pvalues = np.asarray(pvalues)
    reject = multitest.multipletests(pvalues, fdr, method='fdr_bh')[0]
    n = reject.shape[0]
    X = reject.reshape((n // 4, 4))[:, 0:2]
    P = pvalues.reshape((n // 4, 4))[:, 0:2]
    
    for row in P:
        print(row < .05)
        
if __name__ == '__main__':
    plac.call(main)
