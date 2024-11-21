from molecularIDDeclaration import uvc1_hash_t, uvc1_refgpos_t, uvc1_flag_t
from hashDeclaration import hash2hash, strhash

class MolecularBarcode:
    def __init__(self):
        # Initialization as per the previous class declaration
        self.beg_tidpos_pair = (-1, -1)  # Tuple of uvc1_refgpos_t
        self.end_tidpos_pair = (-1, -1)  # Tuple of uvc1_refgpos_t
        self.qnamestring = ""
        self.umistring = ""
        self.duplexflag = 0x0  # uvc1_flag_t
        self.dedup_idflag = 0x0  # uvc1_flag_t
        self.hashvalue = 0  # uvc1_hash_t
    
    def calcHash(self) -> uvc1_hash_t:
        ret: uvc1_hash_t = 0
        ret += hash2hash(ret, hash2hash(self.beg_tidpos_pair[0], self.beg_tidpos_pair[1]))
        ret += hash2hash(ret, hash2hash(self.end_tidpos_pair[0], self.end_tidpos_pair[1]))
        ret += hash2hash(ret, strhash(self.qnamestring))
        ret += hash2hash(ret, strhash(self.umistring))
        ret += hash2hash(ret, self.duplexflag)
        ret += hash2hash(ret, self.dedup_idflag)
        return ret
