from commonClasses import *
BASE = 31

STATIC_REV_COMPLEMENT = {
    'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
    'a': 't', 't': 'a', 'c': 'g', 'g': 'c'
}

def strnhash(s, n, base=BASE):
    ret = 0
    for i in range(min(n, len(s))):
        ret = ret * base + ord(s[i])
    return ret


def strnhash_rc(s, n, base=BASE):
    ret = 0
    for i in range(min(n, len(s))):
        ret = ret * base + ord(STATIC_REV_COMPLEMENT.get(s[n-i-1], s[n-i-1]))
    return ret


def strhash(s, base=BASE):
    return strnhash(s, len(s), base)


def hash2hash(hash1, hash2):
    return hash1 * ((1 << 31) - 1) + hash2
