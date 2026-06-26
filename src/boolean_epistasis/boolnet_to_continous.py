#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sympy.discrete.transforms import fwht

bnet = ["v1, !v1 | v3",
        "v2, !v1 | v2&!v3",
        "v3, !v2"]
bnet = "\n".join(bnet)



def tt_to_multipolynomial_gf2(tt):

    #here gf2_val are elements of {0,1} and sg_val
    # are elements of {-1,1}

    coefs = [0] * len(tt)
    
    for S in range(len(tt)):

        for T in range(len(tt)):

            if T & S == T:  
                sign = (-1) ** (bin(S & ~T).count('1'))
                coefs[S] += sign * tt[T]
    
    return coefs

    
print(tt_to_multipolynomial_gf2([1,1,1,0]))

def hill_cube(mpoly):

    return

def normalized_hill_cube(mpoly):

    return