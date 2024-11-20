# IS_IOHTS_INCLUDED

from commonClasses import *
import pysam
from collections import namedtuple
from typing import List, Tuple

BedLine = namedtuple('BedLine', ['tname', 'tid', 'beg_pos', 'end_pos', 'region_flag', 'n_reads'])

class BedLineProcessor:
    def __init__(self, tid, beg_pos, end_pos, region_flag, n_reads):
        self.tid = tid
        self.beg_pos = beg_pos
        self.end_pos = end_pos
        self.region_flag = region_flag
        self.n_reads = n_reads

    def is_valid(self):
        return True


def load_bam_records(
    samfile: pysam.AlignmentFile,
    hts_idx: pysam.IndexedReads,
    query_tid: int,
    query_beg: int,
    query_end: int
) -> List[pysam.AlignedSegment]:
    """
    Load BAM records using pysam, given query parameters.

    :param samfile: The opened pysam.AlignmentFile object.
    :param hts_idx: The index for querying the file.
    :param query_tid: Target ID (chromosome index).
    :param query_beg: Start position of the query region.
    :param query_end: End position of the query region.
    :return: A list of pysam.AlignedSegment objects.
    """
    # try:
    #     hts_idx.build()
    #     ref_name = samfile.get_reference_name(query_tid)
    #     alignments = list(samfile.fetch(ref_name, query_beg, query_end))
    #     return alignments

    # except ValueError as e:
    #     print(f"Error fetching BAM records: {e}")
    #     return []

