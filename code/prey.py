#-*- coding: utf8
from __future__ import division, print_function
'''
Statistical test for preying between vectors of visits.
'''

from scipy import stats as ss

import numpy as np
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri 

#Automagic conversion of numpy to R
rpy2.robjects.numpy2ri.activate()

METHODS = ('wilcoxon', 'permutation')

def evidence_prey(visits_obj1_now, visits_obj1_prev, visits_obj2_now, \
        visits_obj2_prev, method='wilcoxon'):
    '''
    Tests if there is evidence that obj1 is preying on obj2. In summary it
    tests if:

    .. ::
    
        median(visits_obj1_now) > median(visits_obj1_prev) AND \
                median(visits_obj2_now) < median(visits_obj1_prev)

    That is, if we see an increase if the visits of object 1 and a
    decrease in the visits of object 2. This only make's sense if 
    both the values of obj1 and obj2 are from the same populatuion. That
    is, if we can perform a paired test.

    This method will return two pvalues. The is based on statistical test
    where the alternative hypothesis is:
    median(visits_obj1_now) > median(visits_obj1_prev), 
    
    while in the second the alternative hypothesis is:
    median(visits_obj2_now) < median(visits_obj1_prev)

    Thus, if **both** pvalues are below the required significance, you
    can say that there is evidence of preying behavior.

    We require that:
    
    .. ::

        len(visits_obj1_now) == len(visits_obj1_prev) == \
                len(visits_obj2_now) == len(visits_obj2_prev)

    Parameters
    ----------
    visits_obj1_now: array like
        the visits for obj1 on the current time tick
    
    visits_obj1_prev: array like
        the visits for obj1 on the previous time tick
    
    visits_obj2_now: array like
        the visits for obj2 on the current time tick
    
    visits_obj2_prev: array line
        the visits for obj2 on the previous time tick
    
    method: string in (wilcoxon, permutation)
        The test to use. Both roughly test differences
        in the median, so changing this should have little effect.
    '''
    
    if method not in METHODS:
        raise ValueError('Must choose from:', ' '.join(METHODS))
    
    visits_obj1_now = np.asanyarray(visits_obj1_now)
    visits_obj1_prev = np.asanyarray(visits_obj1_prev)

    visits_obj2_now = np.asanyarray(visits_obj2_now)
    visits_obj2_prev = np.asanyarray(visits_obj2_prev)

    assert visits_obj1_now.ndim == 1
    assert visits_obj1_now.shape == visits_obj1_prev.shape == \
            visits_obj2_prev.shape == visits_obj2_prev.shape

    if method == 'wilcoxon':
        increase_obj1_pval = \
                wilcoxon_one_sided_gt(visits_obj1_now, visits_obj1_prev)[1]
        
        decrease_obj2_pval = \
                wilcoxon_one_sided_gt(visits_obj2_prev, visits_obj2_now)[1]

    else:
        increase_obj1_pval = \
                permutation_test_one_sided_gt(visits_obj1_now, \
                visits_obj1_prev)[1]
        
        decrease_obj2_pval = \
                permutation_test_one_sided_gt(visits_obj2_prev, \
                visits_obj2_now)[1]
    
    return increase_obj1_pval, decrease_obj2_pval 

def wilcoxon_one_sided_gt(visits_arr1, visits_arr2):
    
    wilcox_test = robjects.r['wilcox.test']
    res = wilcox_test(visits_arr1, visits_arr2, paired=True, correction=False, 
            alternative='greater')
    
    stat = res.rx2('statistic')[0]
    pval = res.rx2('p.value')[0]
    
    return stat, pval

def permutation_test_one_sided_gt(visits_arr1, visits_arr2, \
        num_perm=10000):

    visits_arr1 = np.asanyarray(visits_arr1)
    visits_arr2 = np.asanyarray(visits_arr2)

    n = visits_arr1.shape[0]

    #num_perm permutations for every pair of n elements
    aux = np.random.permutation(num_perm * n * 2)
    P = aux.reshape(2, num_perm * n) % n

    #Compute differences in every permutation using vectorized code
    choices_1 = visits_arr1[P[0]]
    choices_2 = visits_arr2[P[1]]
    diff_choices = choices_1 - choices_2
    
    #Reshape for each permutation to be in rows and compute the median
    #statistic
    D = diff_choices.reshape(num_perm, n)
    stat_arr = np.median(D, axis=1)
    null_hyp_true = stat_arr < 0 

    #null_hyp_true has the times a random permutation had a sum
    #less than zero. That is, number of times the null hypothesis
    #is true for a random permutation.
    #Thus, we can proced to compute the p_value
    #
    #The p_val is the probability of a random permutation preying more than
    #0 visits. If this is high, we can't say that the users are shifting their
    #focus since it is only random chance.
    if null_hyp_true.any():
        stat_expected = -stat_arr[null_hyp_true].mean()
    else:
        stat_expected = 0
    p_val = null_hyp_true.mean()
    return stat_expected, p_val
