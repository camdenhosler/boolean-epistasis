#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sympy import fwht

bnet = ["v1, !v1 | v3",
        "v2, !v1 | v2&!v3",
        "v3, !v2"]
bnet = "\n".join(bnet)



def bnet_to_multipolynomial(bnet):

    #here gf2_val are elements of {0,1} and sg_val
    # are elements of {-1,1}

    def bijection(gf2_val):
        sg_val = 1 - 2 * gf2_val
        return sg_val

    def inv_bijection(sg_val):
        gf2_val = (1 - sg_val) / 2
        return gf2_val
    
    

def hill_cube(mpoly):

    return

def normalized_hill_cube(mpoly):

    return