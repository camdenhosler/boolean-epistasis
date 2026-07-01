import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

def find_C_attractors(G, initial_state,interaction_fn):
    tau = 1
    system_exprs = []
    sorted_nodes = sorted(G.nodes)
    
    global_symbols = {node: sp.Symbol(f'x{node}') for node in sorted_nodes}
    
    t = sp.Symbol('t')
    all_vars = [t] + [global_symbols[node] for node in sorted_nodes] 

    for i in G.nodes:
        x_i = sp.symbols(f'x{i}')
        interaction = interaction_fn(G, i ,global_symbols)
        safe_x_i = sp.Max(0,x_i)
        ode = (-safe_x_i+interaction) / tau
        system_exprs.append(ode)
    system = sp.lambdify(all_vars,system_exprs,'numpy')

    t_span = (0, 10)

    def solve_ivp_wrapper(t, y):
        safe_y = np.clip(y, 0.0, 1.0, None)
        return system(t, *safe_y)

    solution = solve_ivp(solve_ivp_wrapper, t_span, initial_state)
    final_attractor_state = solution.y[:, -1]
    return final_attractor_state, system_exprs