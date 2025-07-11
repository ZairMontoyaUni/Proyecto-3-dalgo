
from collections import defaultdict
from functools import lru_cache
import heapq
import random
import sys

from collections import defaultdict
import heapq

import heapq
import sys
import heapq

def calc_overlap(a, b):
    max_len = min(len(a), len(b))
    for l in range(max_len, 0, -1):
        if a[-l:] == b[:l]:
            return l
    return 0

def find(parents, x):
    if parents[x] != x:
        parents[x] = find(parents, parents[x])
    return parents[x]

def union(parents, a, b):
    pa = find(parents, a)
    pb = find(parents, b)
    if pa != pb:
        parents[pa] = pb
        return True
    return False

def shortest_superstring(strings, top_k=10):
    n = len(strings)
    merged_strings = list(strings)
    parents = list(range(n))
    heap = []
    overlap_cache = {}

    # Inicialmente solo tomamos top_k overlaps para cada string
    for i in range(n):
        candidates = []
        for j in range(n):
            if i != j:
                o = calc_overlap(strings[i], strings[j])
                if o > 0:
                    candidates.append((o, i, j))
        for o, i, j in sorted(candidates, reverse=True)[:top_k]:
            overlap_cache[(i, j)] = o
            heapq.heappush(heap, (-o, i, j))

    while heap:
        neg_olap, i, j = heapq.heappop(heap)
        pi = find(parents, i)
        pj = find(parents, j)

        if pi == pj:
            continue

        olap = -neg_olap
        new_str = merged_strings[pi] + merged_strings[pj][olap:]
        new_index = len(merged_strings)
        merged_strings.append(new_str)
        parents.append(new_index)
        union(parents, pi, new_index)
        union(parents, pj, new_index)

        # Solo buscamos top_k overlaps con cadenas activas
        active = set(find(parents, x) for x in range(len(merged_strings)-1))
        candidates = []
        for k in active:
            if k == new_index:
                continue
            key1 = (k, new_index)
            key2 = (new_index, k)

            if key1 in overlap_cache:
                o1 = overlap_cache[key1]
            else:
                o1 = calc_overlap(merged_strings[k], new_str)
                overlap_cache[key1] = o1
            if o1 > 0:
                candidates.append((o1, k, new_index))

            if key2 in overlap_cache:
                o2 = overlap_cache[key2]
            else:
                o2 = calc_overlap(new_str, merged_strings[k])
                overlap_cache[key2] = o2
            if o2 > 0:
                candidates.append((o2, new_index, k))

        for o, a, b in sorted(candidates, reverse=True)[:top_k]:
            heapq.heappush(heap, (-o, a, b))

    # Buscar el representante que contiene la supercadena final
    for i in range(len(merged_strings)):
        if find(parents, i) == i:
            return merged_strings[i]


def main():
    if len(sys.argv) != 3:
        print("Uso: python generador.py input.txt output.txt")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-16') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        first = infile.readline()
        if not first:
            return
        T = int(first.strip())
        results = []

        for _ in range(T):
            while True:
                header = infile.readline()
                if not header:
                    break
                header = header.strip()
                if header:
                    break
            if not header:
                break
            n, k = map(int, header.split())
            strs = [infile.readline().strip() for _ in range(n)]
            res = shortest_superstring(strs)
            results.append(res)

        outfile.write("\n".join(results) + "\n")

if __name__ == "__main__":
    main()
    