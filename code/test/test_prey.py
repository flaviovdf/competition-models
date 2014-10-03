# -*- coding: utf8
from __future__ import division, print_function

from numpy.testing import assert_equal

from code import prey

import numpy as np

def test_permutation_test():
    '''Tests the permutation test'''

    x = np.array([1, 1, 2, 1, 2, 4, 5], dtype='f')
    y = np.array([.5, .5, 1.01, .5, 2, .48, .3], dtype='f')

    ex, pval = prey.permutation_test_one_sided_gt(x, y)
    ex2, pval2 = prey.permutation_test_one_sided_gt(y, x)
   
    assert ex < 0.1
    assert ex2 > 1
    assert pval < 0.05
    assert (1 - pval2) < 0.05

def test_permutation_test2():
    '''Tests the permutation test'''

    x = np.array([10, 10, 20, 10, 20, 40, 50], dtype='f')
    y = np.array([.5, .5, 1.01, .5, 2, .48, .3], dtype='f')

    ex, pval = prey.permutation_test_one_sided_gt(x, y)
    assert_equal(ex, 0)
    assert_equal(pval, 0)

def test_wilcoxon_test():
    '''Tests the wilcoxon test'''

    x = np.array([1, 1, 2, 1, 2, 4, 5], dtype='f')
    y = np.array([.5, .5, 1.01, .5, 2, .48, .3], dtype='f')

    ex, pval = prey.wilcoxon_one_sided_gt(x, y)
    assert pval < 0.05
    
    ex2, pval2 = prey.wilcoxon_one_sided_gt(y, x)
    assert (1 - pval2) < 0.05

def test_wilcoxon_test2():
    '''Tests the wilcoxon test'''

    x = np.array([10, 10, 20, 10, 20, 40, 50], dtype='f')
    y = np.array([.5, .5, 1.01, .5, 2, .48, .3], dtype='f')

    ex, pval = prey.wilcoxon_one_sided_gt(x, y)
    assert pval < 0.05
