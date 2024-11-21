from commonClasses import uvc1_refgpos_t, uvc1_flag_t, uvc1_hash_t
from typing import Tuple
import hashlib

class MolecularBarcode:
    def __init__(self):
        self.beg_tidpos_pair: Tuple[uvc1_refgpos_t, uvc1_refgpos_t] = (-1, -1)
        self.end_tidpos_pair: Tuple[uvc1_refgpos_t, uvc1_refgpos_t] = (-1, -1)
        self.qnamestring: str = ""
        self.umistring: str = ""

        self.duplexflag: uvc1_flag_t = 0x0
        self.dedup_idflag: uvc1_flag_t = 0x0

        self.hashvalue: uvc1_hash_t = 0

    def createKey(self) -> 'MolecularBarcode':
        mb = MolecularBarcode()

        mb.beg_tidpos_pair = (-1, -1)
        mb.end_tidpos_pair = (-1, -1)
        
        if (self.dedup_idflag & 0x3) == 0x3:
            min2 = min(self.beg_tidpos_pair, self.end_tidpos_pair)
            max2 = max(self.beg_tidpos_pair, self.end_tidpos_pair)
            mb.beg_tidpos_pair = min2
            mb.end_tidpos_pair = max2
        elif (self.dedup_idflag & 0x1) == 0x1:
            mb.beg_tidpos_pair = self.beg_tidpos_pair
        elif (self.dedup_idflag & 0x2) == 0x2:
            mb.end_tidpos_pair = self.end_tidpos_pair

        if (self.dedup_idflag & 0x4) == 0x4:
            mb.qnamestring = self.qnamestring
        else:
            mb.qnamestring = ""
        
        if (self.dedup_idflag & 0x8) == 0x8:
            mb.umistring = self.umistring
        else:
            mb.umistring = ""
        
        mb.duplexflag = self.duplexflag
        mb.dedup_idflag = self.dedup_idflag

        return mb

    def __lt__(self, that: 'MolecularBarcode') -> bool:
        return (self.beg_tidpos_pair < that.beg_tidpos_pair or
                (self.beg_tidpos_pair == that.beg_tidpos_pair and
                 (self.end_tidpos_pair < that.end_tidpos_pair or
                  (self.end_tidpos_pair == that.end_tidpos_pair and
                   (self.qnamestring < that.qnamestring or
                    (self.qnamestring == that.qnamestring and
                     (self.umistring < that.umistring or
                      (self.umistring == that.umistring and
                       (self.duplexflag < that.duplexflag or
                        (self.duplexflag == that.duplexflag and
                         (self.dedup_idflag < that.dedup_idflag or
                          (self.dedup_idflag == that.dedup_idflag and
                           self.hashvalue < that.hashvalue))))))))))))

    def calcHash(self) -> uvc1_hash_t:
        # Concatenate all attributes into a string and calculate a hash
        combined_str = (f"{self.beg_tidpos_pair}{self.end_tidpos_pair}{self.qnamestring}"
                        f"{self.umistring}{self.duplexflag}{self.dedup_idflag}")
        
        # Convert the hash to the same type as uvc1_hash_t
        return uvc1_hash_t(int(hashlib.sha256(combined_str.encode('utf-8')).hexdigest(), 16))
