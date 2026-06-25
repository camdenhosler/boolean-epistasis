#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from attractors import find_attractors


def bool_flip(b):
    return 1 - b

def perturb(bnet, initial_state, node1, node2):
    #the two single perturbations
    first_single = {**initial_state, node1: bool_flip(initial_state[node1])}
    second_single = {**initial_state, node2: bool_flip(initial_state[node2])}

    #the double perturbation, could be done with second_single as well
    double = {**first_single, node2: bool_flip(first_single[node2])}

    #the attractors for the single perturbations
    fs_attractor, _, _ = find_attractors(bnet, first_single)
    ss_attractor, _, _ = find_attractors(bnet, second_single)

    #attractor for double
    d_attractor, _, _  = find_attractors(bnet, double)

    return fs_attractor, ss_attractor, d_attractor