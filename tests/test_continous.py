
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import itertools
import boolean_epistasis.truthtable_to_continuous as tc
import boolean_epistasis.continous_attractors as ca

from sympy import degree
from functools import partial
import numpy as np

def simple_bcubes(tt):

    simple_bcube = tc.bool_cube([
                    ([0,1],[0]),
                    ([0,1],[1]),
                    (tt,[0,1])
                    ])
    
    return simple_bcube

def dict_to_nparray(dict, type):
    key_list = sorted(dict.keys(), key=lambda k: int(k[1:]))
    return np.array([dict[k] for k in key_list], dtype=type)

def test_multilinearity():
    test = True

    all_initial_conditions =  [{"v1": v1, "v2": v2, "v3": v3} 
                                for v1,v2,v3 in itertools.product([0,1],repeat=3)]

    all_tts = itertools.product([0,1],repeat=4)

    interaction = partial(tc.bool_cube)

    for tt in all_tts:
        #random colllection of truth tables looped through
        G = tc.make_graph(([
                    ([0,1,1,1],[0,2]),
                    ([0,1,1,0],[1,2]),
                    (tt,[0,1])
                    ]))
        for cond in all_initial_conditions:
            _, equations = ca.find_C_attractors(G, dict_to_nparray(cond,int), interaction)


    for eq in equations:
        indv_degree = max((degree(eq,gen=x) for x in eq.free_symbols), default=2)
        if indv_degree < 1:
            test = False
    assert test

def test_hill():
    test = True
    assert test