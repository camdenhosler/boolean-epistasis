#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
from perturbations import perturb
from epistasis import epistasis

def simple_bnets(tt):
    """Given a truth table of v3 makes a bnet that pyboolnet 
    can work with. To do so if loops through row by row and
    checks when an output is true.  When it is true it assigns
    an AND between the two values and then continues until it hits
    another row and then creates an OR between the AND of the first
    and the AND of the second row."""

    bool_terms = []

    for indx, (v1_val,v2_val) in enumerate([(0,0),(1,0),(0,1),(1,1)]):
        if tt[indx] == 1:
            bool1 = "v1" if v1_val == 1 else "!v1"
            bool2 = "v2" if v2_val == 1 else "!v2"
            bool_terms.append(f"{bool1} & {bool2}")
    
    if not bool_terms:
        v3_val = "0"
    else:
        v3_val = " | ".join(bool_terms)

    simple_bnet = f"v1,v1\nv2,v2\nv3,{v3_val}"

    return simple_bnet

def main():

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
                fs,ss,d = perturb(simple_bnets(tt),cond,"v1","v2")
                IAS = epistasis(fs,ss,d)
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

if __name__ == "__main__":
    main()