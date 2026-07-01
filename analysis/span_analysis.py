#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import itertools
from typing import NamedTuple
from boolean_epistasis.perturbations import bnet_perturb
from boolean_epistasis.epistasis import in_all_span
from boolean_epistasis.truthtable_to_boolnet import tts_to_bnet
class ActivityMeasure(NamedTuple):
    truth_table: list
    activity: int

def simple_bnets(tt):
    """Given a truth table of v3 makes a bnet that pyboolnet 
    can work with. To do so if loops through row by row and
    checks when an output is true.  When it is true it assigns
    an AND between the two values and then continues until it hits
    another row and then creates an OR between the AND of the first
    and the AND of the second row."""

    simple_bnet = tts_to_bnet([
                    ([0,1],[0]),
                    ([0,1],[1]),
                    (tt,[0,1])
                    ])
    
    return simple_bnet

def simple_spans():

    all_initial_conditions =  [{"v1": v1, "v2": v2, "v3": v3} 
                                for v1,v2,v3 in itertools.product([0,1],repeat=3)]

    all_tts = itertools.product([0,1],repeat=4)

    no_epi_real_results = []
    no_epi_activity_results = []
    no_epi_gf2_results = []

    max_epi_real_results = []
    max_epi_activity_results = []
    max_epi_gf2_results = []

    def always_true(results):
        return len(results) > 0 and all(r == True for r in results)

    def always_false(results):
        return len(results) > 0 and all(r == False for r in results)
    
    for tt in all_tts:
        
        real_results_across_cond = []
        activity_results_across_cond = []
        gf2_results_across_cond = []

        for cond in all_initial_conditions:
            
            try:
                fs,ss,d = bnet_perturb(simple_bnets(tt),cond,"v1","v2")
                IAS = in_all_span(fs,ss,d)
                if IAS is None:
                    continue

            except Exception as e:
                print(f"Error for tt={tt}, cond={cond}: {e}")
                continue

            real_results_across_cond.append(IAS.real)
            activity_results_across_cond.append(IAS.activity)
            gf2_results_across_cond.append(IAS.gf2)

        if always_true(real_results_across_cond):
            no_epi_real_results.append(tt)
        if always_true(activity_results_across_cond):
            no_epi_activity_results.append(tt)
        if always_true(gf2_results_across_cond):
            no_epi_gf2_results.append(tt)
        
        if always_false(real_results_across_cond):
            max_epi_real_results.append(tt)
        if always_false(activity_results_across_cond):
            max_epi_activity_results.append(tt)
        if always_false(gf2_results_across_cond):
            max_epi_gf2_results.append(tt)

    print("-" * 50)
    print("REAL SPAN TRUTH TABLES WITH NO EPISTASIS")
    for res in no_epi_real_results:
        print(res)

    print("-" * 50)
    print("ACTIVITY SPAN TRUTH TABLES WITH NO EPISTASIS")
    for res in no_epi_activity_results:
        print(res)

    print("-" * 50)
    print("FINITE FIELD SPAN TRUTH TABLES WITH NO EPISTASIS")
    for res in no_epi_gf2_results:  
        print(res)
    
    print("-" * 50)
    print("REAL SPAN TRUTH TABLES WITH ALWAYS EPISTASIS")
    for res in max_epi_real_results:
        print(res)

    print("-" * 50)
    print("ACTIVITY SPAN TRUTH TABLES WITH ALWAYS EPISTASIS")
    for res in max_epi_activity_results:
        print(res)

    print("-" * 50)
    print("FINITE FIELD SPAN TRUTH TABLES WITH ALWAYS EPISTASIS")
    for res in max_epi_gf2_results:  
        print(res)

def activity_measure():
    all_initial_conditions =  [{"v1": v1, "v2": v2, "v3": v3} 
                                for v1,v2,v3 in itertools.product([0,1],repeat=3)]

    all_tts = itertools.product([0,1],repeat=4)

    def false_counter(results):
        counter = 0
        for r in results:
            if r == False:
                counter += 1
        return counter

    activity_results_counter = []

    for tt in all_tts:

        activity_results_across_cond = []
        counter=0

        for cond in all_initial_conditions:
            
            try:
                fs,ss,d = bnet_perturb(simple_bnets(tt),cond,"v1","v2")
                IAS = in_all_span(fs,ss,d)
                if IAS is None:
                    continue

            except Exception as e:
                print(f"Error for tt={tt}, cond={cond}: {e}")
                continue

            activity_results_across_cond.append(IAS.activity)

            counter = false_counter(activity_results_across_cond)

        activity_measure_term = ActivityMeasure(truth_table=tt, activity=counter)
        activity_results_counter.append(activity_measure_term)

    print("-" * 50)
    print("ALL ACTIVITY MEASURES")
    for am_term in activity_results_counter:
        print(f"{am_term.truth_table}\n{am_term.activity}")
        print("-" * 50)


def main():
    #simple_spans()
    activity_measure()

if __name__ == "__main__":
    main()