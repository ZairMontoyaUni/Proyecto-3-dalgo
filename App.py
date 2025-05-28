import sys
import time
import random
from functools import lru_cache

def eliminar_redundancias(strs):
    unique = []
    for s in sorted(strs, key=len, reverse=True):
        if not any(s in t for t in unique):
            unique.append(s)
    return unique

@lru_cache(maxsize=None)
def overlap(a, b):
    m = min(len(a), len(b))
    for k in range(m, 0, -1):
        if a.endswith(b[:k]):
            return k
    return 0

def greedy_merge(strs):
    strs = eliminar_redundancias(strs)
    while len(strs) > 1:
        best_i = best_j = -1
        best_ov = -1
        for i in range(len(strs)):
            for j in range(len(strs)):
                if i != j:
                    ov = overlap(strs[i], strs[j])
                    if ov > best_ov:
                        best_ov, best_i, best_j = ov, i, j
        merged = strs[best_i] + strs[best_j][best_ov:]
        # Solo eliminar los dos usados y añadir el nuevo sin llamar a eliminar_redundancias
        strs = [s for idx, s in enumerate(strs) if idx not in (best_i, best_j)]
        strs.append(merged)
    return strs[0]

def greedy_insert(strs):
    pool = eliminar_redundancias(strs)
    s = pool.pop(random.randrange(len(pool)))
    while pool:
        best_t = None
        best_s_new = None
        best_len = float('inf')
        for t in pool:
            ov1 = overlap(s, t)
            cand1 = s + t[ov1:]
            ov2 = overlap(t, s)
            cand2 = t + s[ov2:]
            for cand in (cand1, cand2):
                if len(cand) < best_len:
                    best_len = len(cand)
                    best_s_new = cand
                    best_t = t
        s = best_s_new
        pool.remove(best_t)
    return s

def shortest_superstring(strs, trials=20):
    best = None
    for _ in range(trials):
        order = strs[:]
        random.shuffle(order)
        for alg in (greedy_merge, greedy_insert):
            cand = alg(order)
            if best is None or len(cand) < len(best):
                best = cand
    return best

def main():
    data = sys.stdin
    first = data.readline()
    if not first:
        return
    T = int(first.strip())
    results = []
    for _ in range(T):
        # leer línea no vacía
        while True:
            line = data.readline()
            if not line:
                break
            line = line.strip()
            if line:
                break
        if not line:
            break
        n = int(line.split()[0])
        strs = [data.readline().strip() for _ in range(n)]
        res = shortest_superstring(strs, trials=30)
        results.append(res)
    sys.stdout.write("\n".join(results))

if __name__ == '__main__':
    main()

    
    
    