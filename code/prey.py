#-*- coding: utf8
from __future__ import division, print_function
'''
Statistical test for preying between vectors of visits
'''

from scipy import stats as ss

import numpy as np
    
def permutation_test_ge(visits_arr1, visits_arr2, \
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
    
    #Reshape for each permutation to be in rows and compute the sum
    #statistic
    D = diff_choices.reshape(num_perm, n)
    null_hyp_true = D.mean(axis=1) <= 0 #we can change this to any stat

    #null_hyp_true has the times a random permutation had a sum
    #less than zero. That is, number of times the null hypothesis
    #is true for a random permutation.
    #Thus, we can proced to compute the p_value
    #
    #The p_val is the probability of a random permutation preying more than
    #0 visits. If this is high, we can't say that the users are shifting their
    #focus since it is only random chance.
    p_val = null_hyp_true.mean()
    return p_val
