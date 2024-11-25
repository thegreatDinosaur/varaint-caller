from collections import defaultdict
import numpy as np

# Define required constants
LINK_I1, LINK_I2, LINK_I3P = 1, 2, 3
LINK_D1, LINK_D2, LINK_D3P = 4, 5, 6
UNSIGN2SIGN = lambda x: x  # Replace with actual conversion logic
MAX = max

# Define INDEL_ID
INDEL_ID = 1  # Change this value to dynamically adapt the behavior

# Assumed class for BcfFormat and other types
class BcfFormat:
    def __init__(self):
        self.gapNf = []
        self.gapNr = []
        self.gapSeq = []
        self.gapbAD1 = []
        self.gapcAD1 = []
        self.gc2AD = []
        self.gc2dAD = []
        self.AD2 = [0, 0]  # Assuming 2 strands
        self.ADr = [0, 0]  # Assuming 2 strands
        self.gapNum = [0, 0]  # Assuming 2 strands

# Helper functions
def isSymbolIns(symbol):
    return symbol in [LINK_I1, LINK_I2, LINK_I3P]

def isSymbolDel(symbol):
    return symbol in [LINK_D1, LINK_D2, LINK_D3P]

def posToIndelToData_get(depth_map, refpos, indel):
    # Replace this with actual logic to fetch data from depth map
    return depth_map.get(refpos, {}).get(indel, 0)

def get_indel_string(indel, refpos, refchars, symbol2CountCoverageSet):
    """
    Returns the appropriate representation of the indel based on INDEL_ID.
    """
    if INDEL_ID == 1:
        return indel  # Text-based indel representation
    else:
        return refchars[
            refpos - symbol2CountCoverageSet.getUnifiedIncluBegPosition() : refpos + len(indel)
        ]

def fill_by_indel_info(fmt, symbol2CountCoverageSet, strand, refpos, symbol, bq_tsum_depth, fq_tsum_depth, fq_tsum_depth_c2DP, fq_tsum_depth_c2dDP, refchars, specialflag):
    assert isSymbolIns(symbol) or isSymbolDel(symbol), f"Invalid symbol: {symbol}"

    if isSymbolIns(symbol):
        assert symbol in [LINK_I1, LINK_I2, LINK_I3P], f"Invalid insertion symbol: {symbol}"
    else:
        assert symbol in [LINK_D1, LINK_D2, LINK_D3P], f"Invalid deletion symbol: {symbol}"

    assert refpos in bq_tsum_depth, f"Reference position {refpos} not found in bq_tsum_depth"

    bqfq_depth_mutform_tuples = []
    for indel, data in bq_tsum_depth.get(refpos, {}).items():
        indelstring = get_indel_string(indel, refpos, refchars, symbol2CountCoverageSet)
        
        if not indelstring:
            continue

        bqdata = posToIndelToData_get(bq_tsum_depth, refpos, indel)
        fqdata = posToIndelToData_get(fq_tsum_depth, refpos, indel)
        fqdata_c2DP = posToIndelToData_get(fq_tsum_depth_c2DP, refpos, indel)
        fqdata_c2dDP = posToIndelToData_get(fq_tsum_depth_c2dDP, refpos, indel)

        assert bqdata > 0, f"bqdata should be greater than 0: {bqdata}"

        bqfq_depth_mutform_tuples.append((fqdata, bqdata, fqdata_c2DP, fqdata_c2dDP, indelstring))

    gapbAD1sum = 0
    gapcAD1sum = 0
    bqfq_depth_mutform_tuples.sort(reverse=True, key=lambda x: x[1])  # Sorting by bqdata, for example

    gapN = fmt.gapNf if strand == 0 else fmt.gapNr
    gapN.append(len(bqfq_depth_mutform_tuples))

    prev_gapseq_len = 0
    prev_gap_cAD = 0
    maxdiff = 0

    for bqfq_depth_mutform in bqfq_depth_mutform_tuples:
        gap_seq = bqfq_depth_mutform[4]  # Assuming gap_seq is the 5th element
        assert len(gap_seq) > 0, "Gap sequence is empty"

        gap_cAD = bqfq_depth_mutform[1]
        gap_cAD2 = bqfq_depth_mutform[2]
        gap_cAD3 = bqfq_depth_mutform[3]
        gap_bAD = bqfq_depth_mutform[0]

        fmt.gapSeq.append(gap_seq)
        fmt.gapbAD1.append(gap_bAD)
        fmt.gapcAD1.append(gap_cAD)
        fmt.gc2AD.append(gap_cAD2)
        fmt.gc2dAD.append(gap_cAD3)

        if UNSIGN2SIGN(len(gap_seq)) != prev_gapseq_len and prev_gap_cAD > gap_cAD:
            maxdiff = MAX(maxdiff, prev_gap_cAD - gap_cAD)

        prev_gapseq_len = len(gap_seq)
        prev_gap_cAD = gap_cAD

        gapbAD1sum += gap_bAD
        gapcAD1sum += gap_cAD

    return max(maxdiff, prev_gap_cAD), gapcAD1sum
