
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
    
"""def main():
    casos = [
        { 'input': ['aab','baa','aaa','bbb'], 'esperada_len': 7 },
        { 'input': ['abc','bcd','cde'],       'esperada_len': 5 },
        { 'input': ['aab','baa','aaa','bbb','ab','b','bb','a'], 'esperada_len': 7},
        { 'input': ['nfid', 'conf', 'cial', 'denc', 'onfi', 'enci'], 'esperada_len':12},
        {'input': ['piz', 'efb', 'bjw', 'mfl', 'ngq', 'wim', 'drd', 'wad', 'hwv', 'xjg'],
         'esperada_len': 23},
        {'input': [
        'jge', 'agc', 'fbk', 'kle', 'lqy', 'rjb', 'kiw', 'vir', 'bsg', 'owk',
        'rnd', 'pdf', 'prp', 'kpg', 'brf', 'inj', 'jqn', 'emm', 'vde', 'epw',
        'tfs', 'jwk', 'zcg', 'igb', 'gmw', 'krs', 'btc', 'aed', 'iny', 'gfj',
        'jxc', 'emd', 'cjh', 'emj', 'idv', 'qgz', 'adu', 'cmg', 'kmf', 'vrb',
        'fvu', 'bbg', 'mao', 'niz', 'btb', 'eex', 'bps', 'cqo', 'nzn', 'imh',
        'nqf', 'mcy', 'jvl', 'tvl', 'exe', 'wdx', 'uli', 'ipa', 'aho', 'ziq',
        'uzc', 'gsy', 'hwb', 'ojv', 'vwr', 'acq', 'pze', 'wgr', 'cbf', 'jbo',
        'rbh', 'dqw', 'hxs', 'kwj', 'jsb', 'cyz', 'crx', 'ilf', 'lic', 'rqb',
        'qld', 'lzw', 'nxo', 'yjg', 'jhf', 'oqw', 'trk', 'tis', 'vqv', 'fyk',
        'cfd', 'dvt', 'cmi', 'gvt', 'ugl', 'vty', 'tnd', 'vhm', 'teo', 'vly'
        ], 'esperada_len': 217},
        {'input': ["hmz", "bue", "aqe", "xgr", "ogl", "sma", "yob", "rex", "jlu", "hjz",
"ccd", "xne", "drk", "jdw", "enc", "ycy", "nol", "bki", "qjy", "ava",
"fhd", "znx", "lgb", "uri", "mcl", "ftz", "mpa", "vum", "mtj", "gsj",
"bci", "mri", "sok", "qax", "yyg", "kbf", "lso", "hlp", "enw", "nit",
"gak", "wwl", "szl", "vad", "dst", "xko", "klk", "icw", "ghs", "oiw",
"vdl", "sko", "exx", "ywq", "tpk", "tuk", "spq", "dfg", "kqy", "ybl",
"nbo", "qoz", "qyn", "tbr", "zlx", "udf", "syx", "xxc", "zmn", "aay",
"mcg", "qsh", "kyd", "ggv", "uvv", "grr", "vyz", "htw", "mpi", "oph",
"biw", "ycr", "gjh", "qda", "sny", "rhw", "pbb", "zwm", "isd", "nul",
"jzw", "anu", "vdo", "ujn", "lfg", "fcf", "bhz", "vui", "wjw", "nsu",
"snf", "nrq", "crl", "nyb", "yhk", "pyp", "xkh", "urm", "wfm", "wzm",
"buj", "kdc", "gaz", "dtz", "rkv", "aih", "fga", "wjd", "ypb", "dgz",
"vlz", "jzp", "aqf", "vzf", "aho", "xtz", "khb", "zft", "bnz", "tqk",
"spf", "jsw", "mth", "dvu", "jzj", "rlt", "rju", "uik", "oxg", "bgv",
"caj", "byo", "ece", "nzx", "aqu", "cer", "prr", "wdv", "oxy", "fdm",
"rmu", "jij", "jfa", "dxq", "rej", "dze", "jjx", "nuc", "xmq", "uub",
"mfq", "fnd", "vfz", "rof", "xuj", "jly", "uss", "cre", "okg", "kgo",
"hkc", "yyc", "kea", "dar", "gxq", "wgq", "tsq", "cfn", "ieb", "tcr",
"xgc", "rjb", "jmu", "lfj", "blw", "gai", "bxe", "ffw", "wtt", "aet",
"tfg", "ogp", "jte", "vaf", "gki", "xxo", "ujm", "hdo", "akk", "zrr",
"vwx", "uli", "xyv", "dpk", "nch", "wkv", "bcd", "squ", "aab", "fsn",
"dst", "mvb", "wza", "mks", "oiw", "weo", "hdm", "ysw", "jde", "ohj",
"hcb", "ecd", "tuq", "meg", "ngd", "hnu", "tsy", "yil", "mcc", "kaa",
"twq", "zna", "uam", "kqg", "eyg", "cme", "zmi", "fjk", "mvv", "tcq",
"rxr", "qsu", "bnv", "ngg", "vsc", "ckr", "vsm", "uph", "xvs", "bjj",
"zxd", "pcx", "wjo", "cbd", "rzv", "qor", "pqi", "txi", "okp", "kim",
"yzf", "bis", "fqy", "zph", "dth", "wac", "onj", "rsp", "xgi", "osi",
"euv", "kev", "zta", "dym", "wpo", "xhx", "llm", "zpg", "rwx", "umm",
"qnx", "bjg", "xhg", "iun", "zhs", "nwa", "pnm", "shz", "xiv", "dxj",
"cyi", "ahi", "sqb", "qug", "xme", "mub", "pte", "ata", "dwd", "bgb",
"aae", "ygt", "miv", "uuc", "yma", "foc", "qoh", "rlk", "yiw", "tsm",
"eso", "mee", "yio", "msn", "luf", "tbp", "irv", "elf", "nwc", "kkb",
"utw", "uvk", "ppi", "fkd", "zyd", "tje", "jfz", "uic", "zpo", "xex",
"xwt", "nei", "cnh", "bad", "ufx", "qia", "msz", "yey", "oad", "ghe",
"utq", "vdb", "cjf", "lip", "pch", "hkq", "hjx", "pfw", "lgi", "pbi",
"swq", "xxt", "ebv", "aeh", "ihv", "oqg", "dkj", "qcq", "yro", "rse",
"qeq", "esz", "ipz", "nwi", "san", "obz", "ipa", "mka", "qiz", "nyj",
"tah", "dqd", "wlz", "ycd", "inl", "htd", "bkk", "onw", "wso", "khs",
"uqz", "ejp", "jvb", "kfz", "nnw", "yco", "vlx", "lrs", "tll", "fvp",
"qex", "mws", "ogi", "eym", "hxq", "keu", "aws", "kau", "pmw", "dgz",
"orw", "gut", "eiu", "nnr", "iya", "cuk", "hzt", "rmu", "det", "vjg",
"vwf", "fuz", "mbw", "lbh", "lkz", "apl", "inf", "yns", "jrv", "cwa",
"ywo", "qwe", "wxc", "gip", "uie", "pec", "mmo", "qns", "yna", "sou",
"lkm", "rns", "ywc", "xjf", "icw", "mhz", "vnk", "jlp", "eyu", "aei",
"uhm", "gib", "col", "uyy", "zlh", "srs", "mho", "nwe", "kpm", "lec",
"jvc", "xgf", "oce", "mql", "wry", "cpd", "zwa", "pvj", "mqh", "igd",
"pdt", "ijc", "sbw", "dec", "btx", "hex", "elt", "grl", "kzb", "lkf",
"igy", "hci", "tvl", "qcx", "fpo", "ufo", "rdb", "sse", "nvf", "pqi",
"bst", "xru", "wxh", "qyw", "boc", "rxg", "vdn", "twu", "ycq", "aav",
"pkb", "mhr", "dmr", "wvq", "vox", "jyh", "wna", "mcw", "zqm", "egd",
"ean", "set", "tge", "epq", "dkq", "vwx", "nlm", "qfb", "mmx", "iml",
"vkd", "wbo", "wra", "xcr", "fgw", "mmj", "usx", "nuk", "ley", "hpg",
"hfo", "kis", "ang", "qly", "dfz", "dyi", "qyw", "pdc", "ohs", "ltn",
"ice", "rge", "dcl", "osf", "fpm", "axo", "pxl", "lua", "xcf", "zwp",
"liz", "sun", "oiv", "jpo", "hoy", "lmj", "ixk", "lop", "lmh", "srv",
"xrx", "glf", "xcr", "vmg", "cyz", "uzh", "xbt", "ouy", "afv", "udk",
"nfv", "cxc", "sgm", "eyp", "btz", "nen", "jsb", "zpr", "kes", "sxh",
"krl", "mmg", "ocf", "cvy", "hoo", "uhs", "ans", "djr", "tkc", "uth",
"ugn", "tnn", "aue", "xaf", "zkr", "vyw", "agt", "kuz", "ohy", "kpz",
"dwy", "teo", "jjg", "toe", "tcs", "rrq", "xeh", "anv", "eon", "uvu",
"mqz", "opd", "beg", "mvj", "ahb", "suc", "var", "iat", "dvh", "dpd",
"odc", "cgq", "whu", "hth", "epn", "moj", "rko", "izc", "pcs", "hwe",
"wqr", "iec", "dyi", "slm", "ipp", "qzh", "qsv", "laa", "msu", "llq",
"wbm", "xnk", "rzb", "ogy", "ctz", "mjb", "vdz", "lan", "gqq", "ruv",
"iul", "xaa", "wlk", "hnl", "xkp", "lnu", "hgq", "qvb", "bwz", "jew",
"nvm", "kaq", "ycs", "yuq", "bbe", "maz", "pfm", "nue", "yyk", "nwj",
"mct", "bof", "hfk", "igg", "wry", "oot", "ols", "gwd", "jcy", "crf",
"iry", "aom", "ere", "rry", "wjg", "gbn", "npm", "lnj", "duz", "clw",
"zee", "zvq", "mdq", "oxa", "rws", "tyy", "cna", "htd", "gwd", "vfx",
"hlj", "brh", "nro", "tkc", "sxu", "kkw", "ped", "yvz", "vtd", "vsd",
"cda", "agc", "alp", "iqf", "cmq", "nwo", "ufq", "izh", "rca", "phn",
"hip", "zpz", "jut", "xnh", "gnh", "bzq", "tzy", "crv", "kyd", "qwq",
"djf", "zeh", "owm", "btw", "iku", "yrv", "rmx", "woi", "jfc", "mmu",
"smm", "hts", "lqg", "ppj", "lva", "qev", "oer", "hvw", "joe", "adf",
"kvz", "npr", "bbq", "ijy", "zzn", "nni", "jmy", "qao", "kia", "vii",
"mst", "wjx", "wdu", "lgt", "ikp", "tfc", "qot", "xmm", "upq"
], 'esperada_len': 10000}
    ]

    for idx, caso in enumerate(casos, 1):
        strs = caso['input']
        print(f"\nCaso {idx}: {len(strs)} cadenas")
        start = time.time()
        sol = superstring_heap(strs)
        t = time.time() - start
        print(f" Esperada longitud mínima: {caso['esperada_len']}")
        print(f" Longitud obtenida       : {len(sol)}")
        print(f" Obtenida supercadena    : {sol}")
        print(f" Tiempo de ejecución     : {t:.6f} segundos")"""
