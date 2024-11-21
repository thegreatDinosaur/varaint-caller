from iohtsDeclaration import * 
from commonClasses import * 
import pysam
from typing import List

def is_valid(tid: int, tname: str, beg_pos: int, end_pos: int) -> bool:

    return ((tid >= 0 or len(tname) > 0) and beg_pos < end_pos)

def load_bam_records(
    samfile: pysam.AlignmentFile,
    query_tid: int,
    query_beg: int,
    query_end: int
) -> List[pysam.AlignedSegment]:
    alignments = []
    try:
        ref_name = samfile.get_reference_name(query_tid)
        for aln in samfile.fetch(ref_name, query_beg, query_end):
            alignments.append(aln)
    except ValueError as e:
        print(f"Error querying region: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return alignments
# BedLine, load_bam_records

