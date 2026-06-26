#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools

def tt_to_bnet_layer(tt, inputs):
    """
    Given a truth table output column produces a corresponding layer of
    a pybool bnet. It assumes the truth table begins with all zeroes and ends 
    with all ones where the later variables progesively partition the table 
    into smaller chunks i.e. for a two variable function:
    0 0 f(0,0)
    0 1 f(0,1)
    1 0 f(1,0)
    1 1 f(1,1)
    """

    n = int(len(tt)).bit_length() - 1

    bool_terms = []
    
    for row_idx, v_vec in enumerate(itertools.product([0,1],repeat=n)):
        if tt[row_idx] == 1:
            row_bools = []

            for colm_idx in range(n):
                term = f"v{inputs[colm_idx]}" if v_vec[colm_idx] == 1 else f"!v{inputs[colm_idx]}"
                row_bools.append(term)

            and_string = " & ".join(row_bools)
            bool_terms.append(and_string)
    
    if not bool_terms:
        f_val = "0"
    else:
        f_val = " | ".join(bool_terms)

    return f_val

def tts_to_bnet(list_of_tts):
    """
    Given a truth table of something of the form: [([b1,b2,...,bn],[#1,#2,...,#m])...]
    where each bn is a boolean value either 1 or 0 and each #m is any integer outputs
    a corresponding boolean network in pyboolnet string form.  An example of a correct
    input is:
    [([0,1],[1]),
    ([0,1],[2]),
    ([0,1,1,0],[1,2])]
    where the first lists in each tuple correspond to the truth tables and the second
    the nodes which represent each truth tables column in acesending order.
    """
    bnet = ""

    for var, term in enumerate(list_of_tts):
        bnet += "v" + str(var + 1) + ", " + tt_to_bnet_layer(term[0],term[1]) + "\n"
        
    return bnet