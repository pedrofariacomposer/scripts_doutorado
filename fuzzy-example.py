from math import log, factorial, e
rit = [1, 0.5, 1, 0.5, 1, 0.25, 0.25, 1, 0.5]
rit = [2,1,0,0,0,1,2,2,1,1,2]
contours = [
    [0,0,0],
    [1,1,0],
    [0,0,1],
    [0,1,2],
    [0,1,1],
    [0,2,1],
    [0,1,0],
    [1,2,0],
    [2,1,0],
    [1,0,0],
    [2,0,1],
    [1,0,1],
    [1,0,2]
]

def three_groups(rit):
    groups = []

    i = 0
    while i < len(rit):
        if i+3 <= len(rit):
            group = rit[i:i+3]
            groups.append(group)
            i += 2
        else:
            group = rit[i:]
            if len(group) > 1:
                groups.append(group)
            
            i += len(rit)
    return groups

def contour(group):
    return [sorted(list(set(group))).index(x) for x in group]

groups = three_groups(rit)
g_cs = [contour(g) for g in groups]

h_three = 0
base = e
for c in contours:
    c_count = g_cs.count(c) / len(groups)
    if c_count != 0:
        c_log = log(c_count, base)
        pg = c_count * c_log
        h_three += pg

x = (- 1 * h_three) / log(len(contours))
print(groups)
