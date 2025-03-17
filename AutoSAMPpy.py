from __future__ import division
import numpy as np
import pandas as pd
import random
import os
import csv
from inputs_framework import *

# latin_hypercube_sampling is a function created to perform Latin hypercube Sampling of input parameters #

def latin_hypercube_sampling(n, min_range, max_range):

    low = np.arange(0, n) / n
    high = np.arange(1, n + 1) / n
    points = np.random.uniform(low, high, n)
    pointval = list((points * (max_range - min_range)) + min_range)
    return pointval

# generate_raindataset is a function created to generate datasets containing samples of rainfall intenisty #

def generate_raindataset(runs):
    
    intensity_samples = latin_hypercube_sampling(runs, low_rainfallintensity, high_rainfallintensity)
    df = pd.DataFrame(intensity_samples, columns=['Intensity'])
    df.to_csv(intensitydata, index=False)

generate_raindataset(runs_hydrologic)

# generate_lcndataset is a function created to generate landcover datasets #

def generate_lcndataset(runs, lcndata, land_cover_ranges):
    
    land_cover_data = {}
    
    #Generate samples for each land cover type#
    for land_cover, range_values in land_cover_ranges.items():
        samples = np.around(latin_hypercube_sampling(runs, *range_values), decimals=3)
        land_cover_data[land_cover] = samples.tolist()
    # shuffling and prepare dataset #
    for samples in land_cover_data.values():
        random.shuffle(samples)
    
    lc_manningsn_records = list(zip(*land_cover_data.values()))
    lcnarray = np.array(lc_manningsn_records)
    lcndataset = pd.DataFrame(lcnarray, columns=land_cover_data.keys())
    lcndataset_unq = lcndataset.drop_duplicates()
    lcndataset_unq.to_csv(lcndata, index=False)

generate_lcndataset(runs_hydraulic, lcndata, land_cover_ranges) #generate landcover dataset#


