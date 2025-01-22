from contours import *
from math import log, factorial, e

def group_rhythm(rhythm, size, next_group):
    groups = []

    i = 0
    while i < len(rhythm):
        if i+size <= len(rhythm):
            group = rhythm[i:i+size]
            groups.append(group)
            i += next_group
        else:
            i += len(rhythm)
    return groups

def complexity(rhythm, size=3, next_group=2, contours=None):
    groups = group_rhythm(rhythm, size=size, next_group=next_group)
    if contours:
        contours = contours
    else:
        contours = all_contours(size)
    contours_groups = [contour(el) for el in groups]
    h_three = 0
    for c in contours:
        c_count =  contours_groups.count(c) / len(groups)
        if c_count != 0:
            c_log = log(c_count)
            pg = c_count * c_log
            h_three += pg

    return round((- 1 * h_three) / log(len(contours)), 3)


