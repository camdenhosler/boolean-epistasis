#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .truthtable_to_continuous import tt_to_coefs
def hyper_metric(list_of_tts):
    list_of_hms = []

    for tts in list_of_tts:
        inputs = tts[1]
        coefs = tt_to_coefs(tts[0])
        n = len(inputs)+1
        non_higher_terms = coefs[:n]
        linear_terms = non_higher_terms[1:]
        higher_terms = coefs[n:]
        linear_measure = sum(abs(terms) for terms in linear_terms)
        higher_measure = sum(abs(terms) for terms in higher_terms)
        try: 
            hyper_metric = higher_measure / (linear_measure + higher_measure)
            list_of_hms.append(hyper_metric)
        except ZeroDivisionError:
            list_of_hms.append(0.0)

    return list_of_hms
