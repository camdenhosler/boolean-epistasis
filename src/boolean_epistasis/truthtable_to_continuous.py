import networkx as nx

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

def bit_reversal(num, bit_width):
    result = 0
    for _ in range(bit_width):
        result = result << 1 | num & 1
        num >>= 1
    return result

def bool_cube(G,current_node,global_symbols):
    #make k and n lists eventually
    tt = G.nodes[current_node]['truth_table']
    inputs = G.nodes[current_node]['inputs']

    coefs = tt_to_coefs(tt)
    mpoly_terms = []
    n_vars = len(inputs)

    vars = [global_symbols[nbr] for nbr in inputs]

    for idx, coef in enumerate(coefs):
        if coef == 0:
            continue

        term = coef
        #watch out for time complexity here
        for var in range(n_vars):
            if (bit_reversal(idx, n_vars) >> var) & 1:
                term *= vars[var]
        
        mpoly_terms.append(term)

    return sum(mpoly_terms)

def hill_cube(G,current_node,global_symbols,k=0.5,n=13):
    #make k and n lists eventually
    tt = G.nodes[current_node]['truth_table']
    inputs = G.nodes[current_node]['inputs']

    coefs = tt_to_coefs(tt)
    hillpoly_terms = []
    n_fns = len(inputs)

    vars = [global_symbols[nbr] for nbr in inputs]

    hills = [var**n / (k**n + var**n) for _, var in enumerate(vars)]

    for idx, coef in enumerate(coefs):
        if coef == 0:
            continue

        term = coef
        #watch out for time complexity here
        for fn in range(n_fns):
            if (bit_reversal(idx, n_fns) >> fn) & 1:
                term *= hills[fn]
        
        hillpoly_terms.append(term)

    return sum(hillpoly_terms)

def normalized_hill_cube(G,current_node,global_symbols,k=0.5,n=13):
    #make k and n lists eventually
    tt = G.nodes[current_node]['truth_table']
    inputs = G.nodes[current_node]['inputs']

    coefs = tt_to_coefs(tt)
    normhillpoly_terms = []
    n_fns = len(inputs)

    vars = [global_symbols[nbr] for nbr in inputs]

    hills = [var**n / (k**n + var**n) for _, var in enumerate(vars)]
    normalized_hills = []
    for idx, fn in enumerate(hills):
        current_x = vars[idx]
        normalize_coef = fn.evalf(5, subs={current_x: 1})
        normalized_hills.append(fn / normalize_coef)

    for idx, coef in enumerate(coefs):
        if coef == 0:
            continue

        term = coef
        #watch out for time complexity here
        for fn in range(n_fns):
            if (bit_reversal(idx, n_fns) >> fn) & 1:
                term *= normalized_hills[fn]
        
        normhillpoly_terms.append(term)

    return sum(normhillpoly_terms)

def make_graph(list_of_tts):
    G = nx.DiGraph()
    for node_i, (tt,nbrs) in enumerate(list_of_tts):
        G.add_node(node_i,truth_table=tt,inputs=nbrs)

    for node_i, (_, nbrs) in enumerate(list_of_tts):
        for nbr in nbrs:
            G.add_edge(nbr, node_i)
    
    return G