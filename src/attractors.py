#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyboolnet.file_exchange import bnet2primes
from pyboolnet.state_transition_graphs import successor_synchronous

def state_to_key(state):
    return frozenset(state.items())

def find_attractors(bnet,initial_state):

    primes = bnet2primes(bnet)

    #path is a list of visited states and visited is a set of visited states
    path = []
    visited = set()

    current_state = initial_state
    step = 0

    while True:

        key = state_to_key(current_state)
        if key in visited:
            cycle_start = next(i for i, s in enumerate(path) if state_to_key(s) == key )

            transient = path[:cycle_start]
            attractor = path[cycle_start:]
            
            break
            

        visited.add(key)
        path.append(current_state)

        current_state = successor_synchronous(primes, current_state)
        step += 1

    return attractor, transient, step