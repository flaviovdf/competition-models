#-*- coding: utf8
from __future__ import division, print_function

from collections import OrderedDict
from code import db
from scipy import optimize as optim

import lmfit
import numpy as np
import pandas as pd
import plac

#Not the best option since the data does not begin 
#at midnight, but it works.
DAY = 60 * 60 * 24

def get_count_dicts(table_name, daily=True):

    indicator_burst = {}
    burst_start_end = {}
    obj_to_bursts = {}

    objects_to_user = {}
    user_count = {}

    last_seen = {}

    trace_size = 0
    last_tstamp = 0
    for tstamp, user, obj in db.iter_sorted(table_name):
        
        if user not in indicator_burst:
            indicator_burst[user] = OrderedDict()
            indicator_burst[user][0] = obj
            
            burst_start_end[user] = OrderedDict()
            burst_start_end[user][0] = tstamp
            
            obj_to_bursts[user] = {}
            obj_to_bursts[user][obj] = set()
            obj_to_bursts[user][obj].add(0)

            user_count[user] = 0

        curr_burst = len(indicator_burst[user]) - 1
        new_burst = False

        #TODO: really ugly code. fix. If daily we start a new burst
        #if more than a day passed or if the object was not seen that day
        if daily: 
            if (user, obj) in last_seen:
                last_tick_obj_user = last_seen[user, obj]
                
                if obj != indicator_burst[user][curr_burst] and \
                        (tstamp - last_tick_obj_user) >= DAY:
                    new_burst = True
            else:
                new_burst = True

            burst_begin = burst_start_end[user][curr_burst]
            if (tstamp - burst_begin) >= DAY:
                new_burst = True

        #when not daily, we always start a new burst when the obj changes
        elif obj != indicator_burst[user][curr_burst]:
            new_burst = True

        if new_burst: 
            burst_begin = burst_start_end[user][curr_burst]
            burst_start_end[user][curr_burst] = (burst_begin, tstamp)

            indicator_burst[user][curr_burst + 1] = obj
            burst_start_end[user][curr_burst + 1] = tstamp
        
            if obj not in obj_to_bursts[user]:
                obj_to_bursts[user][obj] = set()

            obj_to_bursts[user][obj].add(curr_burst + 1)

        if obj not in objects_to_user:
            objects_to_user[obj] = set()
        
        user_count[user] += 1
        trace_size += 1
        objects_to_user[obj].add(user)
        last_seen[user, obj] = tstamp
        last_tstamp = tstamp
    
    #Close last burst
    for user in indicator_burst:
        curr_burst = len(indicator_burst[user]) - 1
        prev_begin = burst_start_end[user][curr_burst]
        burst_start_end[user][curr_burst] = (prev_begin, last_tstamp)

    return indicator_burst, burst_start_end, obj_to_bursts, objects_to_user, \
            user_count, trace_size

def uni_prior_after_release(t_release, t_start, t_end, params):
    
    if t_end < t_release:
        return 0
    else:
        return 1

def no_prior(t_release, t_start, t_end, params):
    return 1

def prior_exponential(t_release, t_start, t_end, params):

    if t_end < t_release:
        return 0

    if t_start < t_release:
        t_start = t_release
    
    rate = params[0]
    prob_geq_start = np.exp(-rate * (t_start - t_release))
    prob_geq_end = np.exp(-rate * (t_end - t_release))
    
    return prob_geq_start - prob_geq_end

def compute_prob(params, obj, obj_to_bursts, obj_to_users, burst_start_end, \
        prob_users, t_release, normalize, prior):
    
    prob = 0
    users = obj_to_users[obj]
    
    for user in users:
        prob_bursts_given_user = 0
        bursts = obj_to_bursts[user][obj]
        
        for burst in bursts:
            t_start, t_end = burst_start_end[user][burst]
            prob_bursts_given_user += prior(t_release, t_start, t_end, params)
        
        if normalize:
            prob_bursts_given_user = prob_bursts_given_user / len(bursts)

        prob += prob_users[user] * prob_bursts_given_user

    return prob

def fmax(params, obj, obj_to_bursts, obj_to_users, burst_start_end, \
        prob_users, release_date, normalize, prior):

    return -1 * compute_prob(params, obj, obj_to_bursts, obj_to_users, \
            burst_start_end, prob_users, release_date, normalize, prior)

def get_user_prob(users_prob_based_on_freq, user_count, trace_size, 
        users_to_consider=None):

    #Probability of users
    if users_prob_based_on_freq:
        prob_users = np.zeros(len(user_count))
        for user in user_count:
            prob_users[user] = user_count[user] / trace_size
    else:
        prob_users = np.ones(len(user_count)) / len(user_count)
    
    if users_to_consider:
        for user in xrange(prob_users.shape[0]):
            if user not in users_to_consider:
                prob_users[user] = 0

    return prob_users

def get_probs_all_obj_wprior(params, obj_to_bursts, obj_to_users, \
        burst_start_end, prob_users, release_date, normalize, prior):
    
    prob_obj = np.zeros(len(obj_to_users))
    
    for obj in xrange(prob_obj.shape[0]):
        prob_obj[obj] = compute_prob(params, obj, obj_to_bursts, \
                obj_to_users, burst_start_end, prob_users, \
                release_date, normalize, prior)

    prob_obj /= prob_obj.sum()
    return prob_obj

def maximize_for_obj_event(obj_event, obj_to_bursts, obj_to_users, \
        burst_start_end, prob_users, release_date, normalize, prior):

    max_prob = 0
    max_params = None
    init_guess = [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1]
    for init_guess in init_guess:
        init_params = np.array([init_guess])
        opt = optim.minimize(fmax, init_params, \
                args=(obj_event, obj_to_bursts, obj_to_users, burst_start_end, \
                prob_users, release_date, normalize, prior))
        
        params = opt.x
        value = -opt.fun
        if value > max_prob:
            max_prob = value
            max_params = params

    return max_params

def experiment_one(release_name, release_date, indicator_burst, \
        burst_start_end, obj_to_bursts, obj_to_users, \
        user_count, trace_size, id2name, name2id):
    
    release_obj = name2id[release_name]

    #Get the probability of users
    users_prob_based_on_freq = False
    users_to_consider = obj_to_users[release_obj]
    
    #users_prob_based_on_freq = True
    #users_to_consider = None

    prob_users = get_user_prob(users_prob_based_on_freq, user_count, \
            trace_size, users_to_consider)

    #Get the probability without adding a prior to the release
    prob_obj_no_prior = get_probs_all_obj_wprior(None, obj_to_bursts, \
            obj_to_users, burst_start_end, prob_users, release_date, True,
            no_prior)
 
    #Maximize probability for release
    max_params = maximize_for_obj_event(release_obj, obj_to_bursts, \
            obj_to_users, burst_start_end, prob_users, release_date, \
            False, prior_exponential)
    
    #Get every probability with the maximized paramaters  
    prob_obj_prior = get_probs_all_obj_wprior(max_params, obj_to_bursts, \
            obj_to_users, burst_start_end, prob_users, release_date, \
            False, prior_exponential)

    print(id2name[release_obj], 'had a probability of', \
            prob_obj_no_prior[release_obj])
    print('It increased to', prob_obj_prior[release_obj], 
            'when assuming exponential burst at release')
    
    diff_probs = prob_obj_prior - prob_obj_no_prior

    print('Top 10 positive changes')
    objs_inv_argsort = diff_probs.argsort()[::-1][:10]
    for obj in objs_inv_argsort:
        print(id2name[obj], 'changed probs from', 
                prob_obj_no_prior[obj], \
                'to', prob_obj_prior[obj])
    print()

    print('Top 10 negative changes')
    objs_inv_argsort = diff_probs.argsort()[:10]
    for obj in objs_inv_argsort:
        print(id2name[obj], 'changed probs from', \
                prob_obj_no_prior[obj], \
                'to', prob_obj_prior[obj])
    
    print()
    print()

def main(table_name):
    
    id2name, name2id = db.get_mappings(table_name)
    indicator_burst, burst_start_end, obj_to_bursts, obj_to_users, \
            user_count, trace_size = get_count_dicts(table_name)
    
    releases = {'Radiohead':[1191974400],
                'Coldplay':[1213228800],
                'Rihanna':[1180573069],
                'Britney Spears':[1227833869]}

    for release_obj in releases:
        for release_date in releases[release_obj]:
            experiment_one(release_obj, release_date, indicator_burst, \
                    burst_start_end, obj_to_bursts, obj_to_users, \
                    user_count, trace_size, id2name, name2id)

if __name__ == '__main__':
    plac.call(main)
