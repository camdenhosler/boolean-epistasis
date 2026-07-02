#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import boolean_epistasis.truthtable_to_continuous as tc
from boolean_epistasis.continous_attractors import find_C_attractors

import sympy as sp
from functools import partial

list_of_tts = [
    ([0,1],[0]),
    ([1,1,1,1,1,0,1,0],[0,1,2]),
    ([1,1,1,1,1,0,1,1],[0,1,2])]
# list_of_tts = [
#     ([0,1],[0]),
#     ([1,1,1,1,1,0,1,0],[0,1,2]),
#     ([1,1,1,1,0,0,1,1],[0,1,2])]
# list_of_tts = [
#      ([0,1],[0]),
#      ([0,1],[1]),
#      ([1,0,0,0],[0,1])]


G = tc.make_graph(list_of_tts)

interaction = partial(tc.bool_cube)
final_state, equations = find_C_attractors(G, [1,1,1], interaction)

print("Generated SymPy Equations:")
for eq in equations:
    print(f"  {eq}")
    
print("\nFinal Attractor State:")
print(f"  {final_state}")

x0, x1, x2 = sp.symbols('x0 x1 x2')

compiled_func = sp.lambdify((x0, x1, x2), equations, modules="numpy")

result = compiled_func(*final_state)

print(f"{result}")
