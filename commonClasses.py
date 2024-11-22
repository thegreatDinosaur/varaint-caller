#purpose of this file is to declare classes and functions that are used in multiple files
#it defines constants, datatypes and provide utility functions and structures defination.

from typing import List, Tuple, Union, Dict, Any
import math
import struct
from collections import namedtuple

# Constants
MGVCF_REGION_MAX_SIZE = 1000
NUM_WORKING_UNITS_PER_THREAD = 8

OUTVAR_GERMLINE = 0x1
OUTVAR_SOMATIC = 0x2
OUTVAR_ANY = 0x4
OUTVAR_MGVCF = 0x8
OUTVAR_ADDITIONAL_INDEL_CANDIDATE = 0x10
OUTVAR_BASE_NN = 0x20
OUTVAR_LINK_NN = 0x40

MAX_STR_N_BASES = 100
MAX_INSERT_SIZE = 2000
DBLFLT_EPS = float(struct.unpack("d", struct.pack("d", 1.1920929e-07))[0])

# Utility Functions
def min_value(x, y):
    return min(x, y)

def max_value(x, y):
    return max(x, y)

def norm_insert_size(isize: int):
    return 0 if abs(isize) >= MAX_INSERT_SIZE else isize

def are_intervals_overlapping(int1min, int1max, int2min, int2max):
    return not ((int1max <= int2min) or (int2max <= int1min))

def phred2nat(x: float) -> float:
    return (math.log(10.0) / 10.0) * x

def nat2phred(x: float) -> float:
    return (10.0 / math.log(10.0)) * x

def frac2phred(x: float) -> float:
    return -(10.0 / math.log(10.0)) * math.log(x)

def phred2frac(x: float) -> float:
    return 10 ** (-x / 10.0)

def numstates2phred(x: float) -> float:
    return (10.0 / math.log(10.0)) * math.log(x)

def phred2numstates(x: float) -> float:
    return 10 ** (x / 10.0)

# Typedef Equivalents
uvc1_unsigned_int_t = int
uvc1_qual_t = int
uvc1_deciphred_t = int
uvc1_readnum_t = int
uvc1_readnum100x_t = int
uvc1_readpos_t = int
uvc1_refgpos_t = int
uvc1_rp_diff_t = int
uvc1_base_t = int
uvc1_base1500x_t = int
uvc1_readnum_big_t = int
uvc1_readpos_big_t = int
uvc1_refgpos_big_t = int
uvc1_qual_big_t = int
uvc1_flag_t = int
uvc1_hash_t = int

# Enum Equivalents
class AssayType:
    AUTO = 0
    CAPTURE = 1
    AMPLICON = 2

ASSAY_TYPE_TO_MSG = ["AUTO", "CAPTURE", "AMPLICON"]

class MoleculeTag:
    AUTO = 0
    NONE = 1
    BARCODING = 2
    DUPLEX = 3

MOLECULE_TAG_TO_MSG = ["AUTO", "NONE", "BARCODING", "DUPLEX"]

class SequencingPlatform:
    AUTO = 0
    ILLUMINA = 1
    IONTORRENT = 2
    OTHER = 3

SEQUENCING_PLATFORM_TO_MSG = ["AUTO", "ILLUMINA", "IONTORRENT", "OTHER"]
SEQUENCING_PLATFORM_TO_NAME = SEQUENCING_PLATFORM_TO_MSG

class PairEndMerge:
    YES = 0
    NO = 1

PAIR_END_MERGE_TO_MSG = ["YES", "NO"]

# Struct Equivalents
class RegionalTandemRepeat:
    def __init__(self):
        self.begpos: uvc1_refgpos_t = 0
        self.tracklen: uvc1_readpos_t = 0
        self.unitlen: uvc1_readpos_t = 0
        self.indelphred: uvc1_qual_t = 43
        self.anyTR_begpos: uvc1_refgpos_t = 0
        self.anyTR_tracklen: uvc1_readpos_t = 0
        self.anyTR_unitlen: uvc1_readpos_t = 0

class RevComplement:
    def __init__(self):
        self.data = {chr(i): chr(i) for i in range(128)}
        self.data.update({
            'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
            'a': 't', 't': 'a', 'c': 'g', 'g': 'c',
        })
        self.table16 = {1: 8 // 1, 2: 8 // 2, 4: 8 // 4, 8: 8 // 8}

    def complement(self, base: str) -> str:
        return self.data.get(base, base)

STATIC_REV_COMPLEMENT = RevComplement()

# Template Function Equivalents
def mathsquare(x: Union[int, float]) -> Union[int, float]:
    return x * x

def non_neg_minus(a: int, b: int) -> int:
    return max(a - b, 0)

def anyuint2hexstring(n: int) -> str:
    return f"{n:0{2 * n.bit_length() // 8}X}"

def compare_diff_less(k1, k2):
    isdiff = (k1 != k2)
    isless = (k1 < k2)
    return isdiff, isless
