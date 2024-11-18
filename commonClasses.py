import math
import sys
from typing import List, Tuple

# Configuration flags (constants)
COMPILATION_ENABLE_XMGOT = 0
COMPILATION_TRY_HIGH_DEPTH_POS_BIAS = 0

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
DBLFLT_EPS = sys.float_info.epsilon

# Platform constants
OPT_ONLY_PRINT_VCF_HEADER = "/only-print-vcf-header/"
OPT_ONLY_PRINT_DEBUG_DETAIL = "/only-print-debug-detail/"
PLAT_ILLUMINA_LIKE = "Illumina/BGI"
PLAT_ION_LIKE = "IonTorrent/LifeTechnologies/ThermoFisher"

# Utility functions
def is_provided(x: str) -> bool:
    return x != "" and x != "."

def isnt_provided(x: str) -> bool:
    return not is_provided(x)

# Conversion functions for Phred, nat, bit, frac, and states
def phred2nat(x: float) -> float:
    return (math.log(10.0) / 10.0) * x

def nat2phred(x: float) -> float:
    return (10.0 / math.log(10.0)) * x

def frac2phred(x: float) -> float:
    return -(10.0 / math.log(10.0)) * math.log(x)

def phred2frac(x: float) -> float:
    return math.pow(10.0, (-x) / 10.0)

def numstates2phred(x: float) -> float:
    return (10.0 / math.log(10.0)) * math.log(x)

def phred2numstates(x: float) -> float:
    return math.pow(10.0, x / 10.0)

# Utility function to check interval overlap
def are_intervals_overlapping(int1min, int1max, int2min, int2max) -> bool:
    return not ((int1max <= int2min) or (int2max <= int1min))

# Define types using Python standard types
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

# Enums and constants
ASSAY_TYPE_TO_MSG = ["AUTO", "CAPTURE", "AMPLICON"]
MOLECULE_TAG_TO_MSG = ["AUTO", "NONE", "BARCODING", "DUPLEX"]
SEQUENCING_PLATFORM_TO_MSG = ["AUTO", "ILLUMINA", "IONTORRENT", "OTHER"]
SEQUENCING_PLATFORM_TO_NAME = ["AUTO", "ILLUMINA", "IONTORRENT", "OTHER"]
PAIR_END_MERGE_TO_MSG = ["YES", "NO"]

# Class to represent a regional tandem repeat
class RegionalTandemRepeat:
    def __init__(self):
        self.begpos = 0
        self.tracklen = 0
        self.unitlen = 0
        self.indelphred = 43
        self.anyTR_begpos = 0
        self.anyTR_tracklen = 0
        self.anyTR_unitlen = 0

# Reverse complement lookup table
class RevComplement:
    def __init__(self):
        self.data = {chr(i): chr(i) for i in range(128)}
        self.data.update({'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'a': 't', 't': 'a', 'c': 'g', 'g': 'c'})
        self.table16 = {1: 8, 2: 4, 4: 2, 8: 1}

STATIC_REV_COMPLEMENT = RevComplement()

# Utility function templates
def mathsquare(x):
    return x * x

def non_neg_minus(a, b):
    return max(a - b, 0)

def anyuint2hexstring(n):
    hexnum2char = "0123456789ABCDEF"
    nchars = 16  # 64-bit unsigned integer as max
    ret = []
    for _ in range(nchars):
        n2 = n & 0xF
        ret.append(hexnum2char[n2])
        n >>= 4
    ret.reverse()
    return ''.join(ret)

def compare_diff_less(k1, k2):
    isdiff = k1 != k2
    isless = k1 < k2
    return isdiff, isless
