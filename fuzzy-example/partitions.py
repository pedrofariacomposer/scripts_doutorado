def accel_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]


def partitions(n):
    return list(accel_asc(n))

def bin_rel(n):
    return (n * (n-1)) / 2

def aglo(part):
    result = 0
    for k in part:
        result += bin_rel(k)
    return result

def disp(part):
    t = bin_rel(sum(part))
    return t - aglo(part)

def lex(n):
    result = []
    for k in range(1,n+1):
        parts = partitions(k)
        for j in parts:
            result.append(j)
    return result

def lex_pairs(n):
    lexicon = lex(n)
    result = []
    for part in lexicon:
        pos_pairs = partitions(sum(part))
        for pos in pos_pairs:
            result.append([part, pos])
    return result



c = sorted(lex_pairs(4), key = lambda x: (len(x[0]), disp(x[0]), len(x[1]), disp(x[1])))
for x in c:
    print(x)