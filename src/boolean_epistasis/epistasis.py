import numpy as np
from typing import NamedTuple

class InAttractorSpan(NamedTuple):
    real: bool
    activity: bool
    gf2: bool

def dict_to_nparray(dict, type):
    key_list = sorted(dict.keys(), key=lambda k: int(k[1:]))
    return np.array([dict[k] for k in key_list], dtype=type)

def in_real_span(att_1, att_2, target_att):
    u = dict_to_nparray(att_1, np.float64)
    v = dict_to_nparray(att_2, np.float64)
    w = dict_to_nparray(target_att, np.float64)
    A = np.column_stack((u,v))
    x, _, _, _ = np.linalg.lstsq(A,w,rcond=None)
    distance = np.allclose(A @ x, w)
    #print(f"  u={u}, v={v}, w={w}, x={x}, result={distance}")
    return distance

def in_activity_span(att_1, att_2, target_att):  
    u = dict_to_nparray(att_1, bool)
    v = dict_to_nparray(att_2, bool)
    w = dict_to_nparray(target_att, bool)
    #here each of these truth tables mark ones in each of the values allowed
    #the below are numpy boolean functions which differ in notation from pybool's
    one_mask = u & v
    zero_mask = ~(u | v)
    any_mask = u ^ v

    if np.any(one_mask & ~w) or np.any(zero_mask & w):
        return False
    else:
        return True

def in_gf2_span(att_1, att_2, target_att):
    u = dict_to_nparray(att_1, bool)
    v = dict_to_nparray(att_2, bool)
    w = dict_to_nparray(target_att, bool)

    zero_vec = np.zeros(len(u), bool)

    #here there are a discrete number of vectors in the span 
    # where each p represents a unique point
    p1 = zero_vec ^ zero_vec
    p2 = u ^ zero_vec
    p3 = zero_vec ^ v
    p4 = u ^ v

    points = [p1,p2,p3,p4]

    if any(np.array_equal(p, w) for p in points):
        return True
    else:
        return False

def epistasis(fs_attractor,ss_attractor,d_attractor):
    """After running tests need to calculate projection length
    as well for both distance from span and then distance from
    sum in the span."""
    if len(fs_attractor) >= 2 or len(ss_attractor) >= 2 or len(d_attractor) >= 2:
        print("Encountered Limit Cycles")
        return None
    else:
        fsfpa = fs_attractor[0]
        ssfpa = ss_attractor[0]
        dfpa = d_attractor[0]
        return InAttractorSpan(
        real = in_real_span(fsfpa,ssfpa,dfpa),
        activity = in_activity_span(fsfpa,ssfpa,dfpa),
        gf2 = in_gf2_span(fsfpa,ssfpa,dfpa)
        )
