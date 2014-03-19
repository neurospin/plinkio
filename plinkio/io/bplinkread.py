# -*- coding: utf-8 -*-

import numpy as np


def bedExpand(b, trail):
    """TODO
    """
    part0 = 0x03
    part1 = 0x0C
    part2 = 0x30
    part3 = 0xC0
    decal0 = 0
    decal1 = 2
    decal2 = 4
    decal3 = 6
    part = [0x03, 0x0C, 0x30, 0xC0]
    decal = [0, 2, 4, 6]
    paire = [0, 1, 2]
    if trail:
        lon = len(b) - 1
    else:
        lon = len(b)
    retval = np.zeros(4*lon + trail, dtype=np.uint8)
    if lon:
        retval[range(0, 4*lon, 4)] = (b & part0) >> decal0
        retval[range(1, 4*lon, 4)] = (b & part1) >> decal1
        retval[range(2, 4*lon, 4)] = (b & part2) >> decal2
        retval[range(3, 4*lon, 4)] = (b & part3) >> decal3
    if trail:
        for i in paire[0:trail]:
            retval[4*lon+i] = (b[-1] & part[i]) >> decal[i]
    return retval


def bedHeader(fn):
    """TODO
    """
    f = open(fn, "rb")
    start = f.read(3)
    if ((start[0] != '\x6C') or (start[1] != '\x1B')):
        print "Input file does not appear to be a .bed file (%s, %s)" % (start[0], start[1])
    snp_major = start[2]
    f.close()
    return snp_major


def bedRead(fn):
    """TODO
    """
    f = open(fn, "rb")
    buf = f.read()  # read the whole dataset
    f.close()
    return np.frombuffer(buf, dtype=np.uint8, offset=3)


def bedDecode(buf, ind, snp, encode, w=None):
    """TODO
    """
    n, trail = ((ind/4+1, ind % 4) if ind % 4 else (ind/4, ind % 4))
    tmp = buf.reshape((-1, n))  # TODO Put a try raise here la deux dim == snp
    if w is None:
        return encode[np.asarray([bedExpand(tmp[x, :], trail) for x in range(tmp.shape[0])]).T]
    else:
        return encode[bedExpand(tmp[w, :], trail)]
