import time
import random

# Función para eliminar redundancias en cualquier lista de cadenas
def eliminar_redundancias(strs):
    unique = []
    for s in sorted(strs, key=len, reverse=True):
        if not any(s in t for t in unique):
            unique.append(s)
    return unique

# 1) Algoritmo greedy por merge de pares con mayor solapamiento
def greedy_merge(strs):
    strs = eliminar_redundancias(strs)
    def overlap(a, b):
        m = min(len(a), len(b))
        for k in range(m, 0, -1):
            if a.endswith(b[:k]):
                return k
        return 0
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
        new_list = [s for idx, s in enumerate(strs) if idx not in (best_i, best_j)]
        new_list.append(merged)
        strs = eliminar_redundancias(new_list)
    return strs[0]

# 2) Algoritmo greedy de inserción en extremos (front/back)
def greedy_insert(strs):
    pool = eliminar_redundancias(strs)
    def overlap(a, b):
        m = min(len(a), len(b))
        for k in range(m, 0, -1):
            if a.endswith(b[:k]): return k
        return 0
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
                cand_pool = [c for c in pool if c != t] + [cand]
                cand_pool = eliminar_redundancias(cand_pool)
                if len(cand) < best_len:
                    best_len, best_s_new, best_t = len(cand), cand, t
        s = best_s_new
        pool.remove(best_t)
        pool = eliminar_redundancias(pool)
    return s

# 3) Multi-start combinando ambos heurísticos
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
    # Modo prueba sin stdin/stdout: casos predefinidos\c
    casos = [
        { 'input': ['aab','baa','aaa','bbb'], 'esperada_len': 7 },
        { 'input': ['abc','bcd','cde'],       'esperada_len': 5 },
        { 'input': ['aab','baa','aaa','bbb','ab','b','bb','a'], 'esperada_len': 7},
    ]
    for idx, caso in enumerate(casos, 1):
        strs = caso['input']
        print(f"Caso {idx}: cadenas = {strs}")
        start = time.time()
        sol = shortest_superstring(strs, trials=30)
        t = time.time() - start
        print(f" Esperada longitud mínima: {caso['esperada_len']}")
        print(f" Obtenida supercadena : {sol}")
        print(f" Longitud obtenida   : {len(sol)}")
        print(f" Tiempo ejecución    : {t:.6f}s\n")

if __name__ == '__main__':
    main()