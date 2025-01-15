from itertools import product


def all_contours(n):
    it = range(n)
    combs = product(it, repeat=n)

    result = []
    for el in combs:
        c = contour(el)
        if c not in result:
            result.append(c)
    return result

def contour(group):
    return [sorted(list(set(group))).index(x) for x in group]