#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from perturbations import perturb
from epistasis import epistasis
bnet_string = """
v1, 1
v2, v2
v3, v2 & (!v1 | v3)
v4, !v3
"""
initial_state_string = {"v1": 1, "v2": 0, "v3": 1, "v4": 0} 

print(perturb(bnet_string, initial_state_string, "v1", "v3"))
fs,ss,d = perturb(bnet_string, initial_state_string, "v1", "v3")
print(epistasis(fs,ss,d))