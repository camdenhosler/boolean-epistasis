import numpy as np
from numpy import ndarray
from typing import NamedTuple

class InAttractorSpan(NamedTuple):
    real: bool
    activity: bool
    gf2: bool
class OrthogonalProjectionDistance:
    real: np.float64
    activity: int
    gf2: int

def dict_to_nparray(dict, type):
    key_list = sorted(dict.keys(), key=lambda k: int(k[1:]))
    return np.array([dict[k] for k in key_list], dtype=type)

def bnet_in_real_span(att_1:ndarray, att_2:ndarray, target_att:ndarray):
    A = np.column_stack((att_1,att_2))
    x, _, _, _ = np.linalg.lstsq(A,target_att,rcond=None)
    if np.allclose(A @ x, target_att):
        return True
    else:
        return False

def bnet_in_activity_span(att_1:ndarray, att_2:ndarray, target_att:ndarray):  
    #here each of these truth tables mark ones in each of the values allowed
    #the below are numpy boolean functions which differ in notation from pybool's
    one_mask = att_1 & att_2
    zero_mask = ~(att_1 | att_2)

    if np.any(one_mask & ~target_att) or np.any(zero_mask & target_att):
        return False
    else:
        return True

def bnet_in_gf2_span(att_1:ndarray, att_2:ndarray, target_att:ndarray):
    zero_vec = np.zeros(len(att_1), bool)

    #here there are a discrete number of vectors in the span 
    # where each p represents a unique point
    p1 = zero_vec ^ zero_vec
    p2 = att_1 ^ zero_vec
    p3 = zero_vec ^ att_2
    p4 = att_1 ^ att_2

    points = [p1,p2,p3,p4]

    if any(np.array_equal(p, target_att) for p in points):
        return True
    else:
        return False

def in_all_span(fs_attractor,ss_attractor,d_attractor):
    if len(fs_attractor) >= 2 or len(ss_attractor) >= 2 or len(d_attractor) >= 2:
        print("Encountered Limit Cycles")
        return None
    else:
        fsfpa = dict_to_nparray(fs_attractor[0],np.float64)
        ssfpa = dict_to_nparray(ss_attractor[0],np.float64)
        dfpa = dict_to_nparray(d_attractor[0],np.float64)
        bool_fsfpa = dict_to_nparray(fs_attractor[0],bool)
        bool_ssfpa = dict_to_nparray(ss_attractor[0],bool)
        bool_dfpa = dict_to_nparray(d_attractor[0],bool)
        return InAttractorSpan(
        real = bnet_in_real_span(fsfpa,ssfpa,dfpa),
        activity = bnet_in_activity_span(bool_fsfpa,bool_ssfpa,bool_dfpa),
        gf2 = bnet_in_gf2_span(bool_fsfpa,bool_ssfpa,bool_dfpa)
        )

def real_projection(att1:ndarray,att2:ndarray,target_att:ndarray):
    A = np.column_stack((att1,att2))
    x, _, _, _ = np.linalg.lstsq(A,target_att,rcond=None)
    return 2

def bnet_projection(att_1:ndarray, att_2:ndarray, target_att:ndarray):  
    one_mask = att_1 & att_2
    zero_mask = ~(att_1 | att_2)
    any_mask = att_1 ^ att_2

    if np.any(one_mask & ~target_att) or np.any(zero_mask & target_att):
        return False
    else:
        return True