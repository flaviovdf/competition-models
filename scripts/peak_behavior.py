#-*- coding: utf8
from __future__ import division, print_function

from code import db

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plac

def main(table_name):
    id2name = db.get_mappings(table_name)[0]
    series = db.get_user_obj_timeseries(table_name)
    
if __name__ = '__main__':
    plac.call(main)
