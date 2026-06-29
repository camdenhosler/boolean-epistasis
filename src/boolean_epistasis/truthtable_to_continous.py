#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sympy as sp

def tt_to_coefs(tt):

    #here gf2_val are elements of {0,1} and sg_val
    # are elements of {-1,1}

    #rewrite with FFT
    coefs = [0] * len(tt)

    for T in range(len(tt)):

        for S in range(len(tt)):
            if T & S == T:  
                sign = (-1) ** (bin(S & ~T).count('1'))
                coefs[S] += sign * tt[T]
    
    return coefs

def bool_cube(coefs):
    mpoly_terms = []
    n_vars = int(len(coefs)).bit_length() - 1

    vars = sp.symbols(f'x0:{n_vars}')

    for idx, coef in enumerate(coefs):
        if coef == 0:
            continue

        term = coef

        for var in range(n_vars):
            if (idx >> var) & 1:
                term *= vars[var]
        
        mpoly_terms.append(term)

    return sum(mpoly_terms), vars

def hill_cube(coefs, k, n):
    #make k and n lists eventually
    hillpoly_terms = []
    n_vars = int(len(coefs)).bit_length() - 1

    vars = sp.symbols(f'x0:{n_vars}')
    hills = [var**n / (k**n + var**n) for i, var in enumerate(vars)]

    for idx, coef in enumerate(coefs):
        if coef == 0:
            continue

        term = coef

        for fn in range(n_vars):
            if (idx >> fn) & 1:
                term *= hills[fn]
        
        hillpoly_terms.append(term)

    return sum(hillpoly_terms), vars

def normalized_hill_cube(coefs, k ,n):
    #make k and n lists eventually
    normhillpoly_terms = []
    n_vars = int(len(coefs)).bit_length() - 1

    vars = sp.symbols(f'x0:{n_vars}')
    hills = [var**n / (k**n + var**n) for i, var in enumerate(vars)]
    
    normalized_hills = []
    for idx, fn in enumerate(hills):
        current_x = vars[idx]  # Use the exact symbol object
        normalize_coef = fn.evalf(30, subs={current_x: 1})
        normalized_hills.append(fn / normalize_coef)

    for idx, coef in enumerate(coefs):
        if coef == 0:
            continue

        term = coef

        for fn in range(n_vars):
            if (idx >> fn) & 1:
                term *= normalized_hills[fn]
        
        normhillpoly_terms.append(term)

    return sum(normhillpoly_terms), vars