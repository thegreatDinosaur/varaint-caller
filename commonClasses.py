import math
import struct
from typing import List, Tuple, Union


# Compilation flags
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

OPT_ONLY_PRINT_VCF_HEADER = "/only-print-vcf-header/"
OPT_ONLY_PRINT_DEBUG_DETAIL = "/only-print-debug-detail/"

PLAT_ILLUMINA_LIKE = "Illumina/BGI"
PLAT_ION_LIKE = "IonTorrent/LifeTechnologies/ThermoFisher"

MAX_STR_N_BASES = 100
MAX_INSERT_SIZE = 2000

DBLFLT_EPS = float(struct.unpack('f', struct.pack('f', 1.0))[0]) - 1.0

# Type Aliases
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


# Enums (Implemented as Python dictionaries)
AssayType = {
    "ASSAY_TYPE_AUTO": 0,
    "ASSAY_TYPE_CAPTURE": 1,
    "ASSAY_TYPE_AMPLICON": 2,
}

MoleculeTag = {
    "MOLECULE_TAG_AUTO": 0,
    "MOLECULE_TAG_NONE": 1,
    "MOLECULE_TAG_BARCODING": 2,
    "MOLECULE_TAG_DUPLEX": 3,
}

SequencingPlatform = {
    "SEQUENCING_PLATFORM_AUTO": 0,
    "SEQUENCING_PLATFORM_ILLUMINA": 1,
    "SEQUENCING_PLATFORM_IONTORRENT": 2,
    "SEQUENCING_PLATFORM_OTHER": 3,
}

PairEndMerge = {
    "PAIR_END_MERGE_YES": 0,
    "PAIR_END_MERGE_NO": 1,
}


# Helper Functions
def phred2nat(x: float) -> float:
    return (math.log(10.0) / 10.0) * x


def nat2phred(x: float) -> float:
    return (10.0 / math.log(10.0)) * x


def frac2phred(x: float) -> float:
    return -(10.0 / math.log(10.0)) * math.log(x)


def phred2frac(x: float) -> float:
    return math.pow(10.0, -x / 10.0)


def numstates2phred(x: float) -> float:
    return (10.0 / math.log(10.0)) * math.log(x)


def phred2numstates(x: float) -> float:
    return math.pow(10.0, x / 10.0)


def mathsquare(x: Union[int, float]) -> Union[int, float]:
    return x * x


def non_neg_minus(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return max(a - b, 0)


def anyuint2hexstring(n: int) -> str:
    return hex(n)[2:].upper()


def are_intervals_overlapping(int1min: int, int1max: int, int2min: int, int2max: int) -> bool:
    return not (int1max <= int2min or int2max <= int1min)


# Structs
class RegionalTandemRepeat:
    def __init__(self):
        self.begpos: uvc1_refgpos_t = 0
        self.tracklen: uvc1_readpos_t = 0
        self.unitlen: uvc1_readpos_t = 0
        self.indelphred: uvc1_qual_t = 40 + 3
        self.anyTR_begpos: uvc1_refgpos_t = 0
        self.anyTR_tracklen: uvc1_readpos_t = 0
        self.anyTR_unitlen: uvc1_readpos_t = 0


class RevComplement:
    def __init__(self):
        self.data = [chr(i) for i in range(128)]
        self.data[ord('A')] = 'T'
        self.data[ord('T')] = 'A'
        self.data[ord('C')] = 'G'
        self.data[ord('G')] = 'C'
        self.data[ord('a')] = 't'
        self.data[ord('t')] = 'a'
        self.data[ord('c')] = 'g'
        self.data[ord('g')] = 'c'
        self.table16 = [i for i in range(16)]
        self.table16[1] = 8 // 1
        self.table16[2] = 8 // 2
        self.table16[4] = 8 // 4
        self.table16[8] = 8 // 8


STATIC_REV_COMPLEMENT = RevComplement()
