from .boolean_attractors import find_B_attractors
from .continous_attractors import find_C_attractors

def bool_flip(b):
    return 1 - b

def bnet_perturb(bnet, initial_state, node1, node2):
    """
    bnet is a pyboolnet graph
    initial_state is a dictionary
    node1 is the key of node1
    node2 is the key of node2
    """
    #the two single perturbations
    first_single = {**initial_state, node1: bool_flip(initial_state[node1])}
    second_single = {**initial_state, node2: bool_flip(initial_state[node2])}

    #the double perturbation, could be done with second_single as well
    double = {**first_single, node2: bool_flip(first_single[node2])}

    #the attractors for the single perturbations
    fs_attractor, _ = find_B_attractors(bnet, first_single)
    ss_attractor, _ = find_B_attractors(bnet, second_single)

    #attractor for double
    d_attractor, _ = find_B_attractors(bnet, double)

    return fs_attractor, ss_attractor, d_attractor

def cont_perturb(G, initial_state, interaction_fn, node1, node2):
    """
    G is networkx graph
    initial_state is list
    interaction_fn is function which has G,current_node,global_symbols
    as inputs and outputs a sympy expression
    node1 is the index of node1
    node2 is the index of node2
    """
    #the two single perturbations
    first_single = initial_state
    second_single = initial_state
    first_single[node1] = bool_flip(initial_state[node1])
    second_single[node2] = bool_flip(initial_state[node2])

    #the double perturbation, could be done with second_single as well
    double = first_single
    double[node2] = bool_flip(first_single[node2])

    #the attractors for the single perturbations
    fs_attractor, _ = find_C_attractors(G, first_single, interaction_fn)
    ss_attractor, _ = find_C_attractors(G, second_single, interaction_fn)

    #attractor for double
    d_attractor, _ = find_C_attractors(G, double, interaction_fn)
    return fs_attractor, ss_attractor, d_attractor