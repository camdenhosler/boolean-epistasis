#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import itertools
from boolean_epistasis.perturbations import cont_perturb
from boolean_epistasis.epistasis import real_projection, dict_to_nparray
import boolean_epistasis.truthtable_to_continuous as tc
from boolean_epistasis.higherorder import hyper_metric

from functools import partial

def main():

    all_tts = itertools.product([0,1],repeat=4)
    all_initial_conditions =  [{"v1": v1, "v2": v2, "v3": v3} 
                                for v1,v2,v3 in itertools.product([0,1],repeat=3)]
    interaction = partial(tc.hill_cube)

    epistasis_vec = []
    hm_vec = []

    for tt in all_tts:
        list_of_tts = [
                    (tt,[0,2]),
                    (tt,[1,2]),
                    (tt,[0,1])
                    ]
        G = tc.make_graph(list_of_tts)
        distance_across_conds = []

        for cond in all_initial_conditions:
            fsfpa, ssfpa, dfpa = cont_perturb(G,dict_to_nparray(cond,int),interaction,0,1)
            real_distance = real_projection(fsfpa,ssfpa,dfpa)
            distance_across_conds.append(real_distance)
        epistasis = sum(distance_across_conds)

        list_of_hms = hyper_metric(list_of_tts)
        hm = list_of_hms[2]

        print("-"*50)
        print(tt)
        print(epistasis)
        print(hm)

        epistasis_vec.append(epistasis)
        hm_vec.append(hm)

        epistasis = 0
        hm = 0
    
if __name__ == "__main__":
    main()
        



