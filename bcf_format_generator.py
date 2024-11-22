import sys

# Constants
BCF_NUM_A = -1
BCF_NUM_R = -2
BCF_NUM_G = -3
BCF_NUM_D = -4

# Enum-like structure for BCF data types
class BCFDataType:
    BCF_STRING = 0
    BCF_INTEGER = 1
    BCF_SIG_INT = 2
    BCF_S64_INT = 3
    BCF_FLOAT = 4
    BCF_SEP = 5
    NUM_BCF_DATA_TYPES = 6

# Python equivalent of the data types
CPP_DATA_STRING = [
    "str",
    "int",    # "uint32_t",
    "int",
    "int",
    "float",
    "bool",
    None
]

CPP_DATA_VALUES = [
    "\"\"",
    "0",
    "0",
    "0",
    "0",
    "False",
    None,
]

BCF_DATA_STRING = [
    "String",
    "Integer",
    "Integer",
    "Integer",  # may overflow
    "Float",
    "String",
    None
]

def vcf_number_to_header_str(num):
    """Convert the BCF number to its header string representation."""
    if num > 0:
        return str(num)
    elif num == BCF_NUM_A:
        return "A"
    elif num == BCF_NUM_R:
        return "R"
    elif num == BCF_NUM_G:
        return "G"
    elif num == BCF_NUM_D:
        return "."
    else:
        sys.stderr.write(f"{num} is not a valid BCF type!\n")
        sys.exit(1)

# FILTER_VEC equivalent in Python as a list of tuples (name, description)
FILTER_VEC = [
    ("noVar", "Not a variant (for example, when REF and ALT are the same), but still included to get all statistics."),
    ("upstreamDel", "Deletion extended from another upstream deletion."),
    ("s50", "Less than 50% of samples have data."),
    ("Q10", "Quality below 10 and no other filters."),
    ("Q20", "Quality below 20 and no other filters."),
    ("Q30", "Quality below 30 and no other filters."),
    ("Q40", "Quality below 40 and no other filters."),
    ("Q50", "Quality below 50 and no other filters."),
    ("Q60", "Quality below 60 and no other filters."),
    ("aInsertSize", "For FORMAT/FTS: Stranded insert bias, meaning the most-supported strand has abnormal insert size at either the left or right end."),
    ("aBQXM", "For FORMAT/FTS: Passing-filter bias, meaning the variant allele is supported by reads with low base qualities at the variant site and/or with high number of mismatches relative to all alleles."),
    ("bcDup", "For FORMAT/FTS: Duplication bias for less-than-expected amplification of variant reads, meaning the variant is under-amplified by PCR relative to all alleles."),
    ("cbDup", "For FORMAT/FTS: Duplication bias for more-than-expected amplification of variant reads, meaning the variant is over-amplified by PCR relative to all alleles."),
    ("aAlignL", "For FORMAT/FTS: Alignment bias on the left mapping coordinate of the sequenced segment relative to all alleles."),
    ("aAlignR", "For FORMAT/FTS: Alignment bias on the right mapping coordinate of the sequenced segment relative to all alleles."),
    ("aPositionL", "For FORMAT/FTS: Position bias on the left mapping coordinate of the sequenced segment relative to all alleles."),
    ("aPositionR", "For FORMAT/FTS: Position bias on the right mapping coordinate of the sequenced segment relative to all alleles."),
    ("abPositionL", "For FORMAT/FTS: Position bias on the left mapping coordinate of the insert relative to all alleles."),
    ("abPositionR", "For FORMAT/FTS: Position bias on the right mapping coordinate of the insert relative to all alleles."),
    ("aStrand", "For FORMAT/FTS: Strand bias relative to all alleles."),
    ("c0Orientation", "For FORMAT/FTS: Read-orientation bias using de-duplicated reads families passing the base-quality threshold for generating UMI-barcode families relative to all alleles."),
    ("c2Orientation", "For FORMAT/FTS: Read-orientation bias using tier-2 UMI-barcode families relative to all alleles."),
    ("c2AlignL", "For FORMAT/FTS: Alignment bias on the left mapping coordinate of the tier-2 single-strand consensus sequence (SSCS) relative to all alleles."),
    ("c2AlignR", "For FORMAT/FTS: Alignment bias on the right mapping coordinate of the tier-2 single-strand consensus sequence (SSCS) relative to all alleles."),
    ("c2PositionL", "For FORMAT/FTS: Position bias on the left mapping coordinate of the tier-2 single-strand consensus sequence (SSCS) relative to all alleles."),
    ("c2PositionR", "For FORMAT/FTS: Position bias on the right mapping coordinate of the tier-2 single-strand consensus sequence (SSCS) relative to all alleles."),
    ("c2StrictPosL", "For FORMAT/FTS: Strictly defined position bias (which has zero prior probability of not having bias) on the left mapping coordinate of the tier-2 single-strand consensus sequence (SSCS) relative to all alleles."),
    ("c2StrictPosR", "For FORMAT/FTS: Strictly defined position bias (which has zero prior probability of not having bias) on the right mapping coordinate of the tier-2 single-strand consensus sequence (SSCS) relative to all alleles."),
]

class BcfFormatStruct:
    def __init__(self, id, in_num_1, out_num_2=None, data_type=None, description=""):
        self.id = id
        self.in_num_1 = in_num_1
        self.out_num_2 = in_num_1 if out_num_2 is None else out_num_2
        self.type = data_type
        self.description = description
        self.is_SSCS_required = False
        self.is_not_in_out_vcf = False

    def sscs(self):
        """Returns a copy of the structure with SSCS flag set to True."""
        ret = self.__copy__()
        ret.is_SSCS_required = True
        return ret

    def not_put_in_vcf(self):
        """Returns a copy of the structure with 'not in vcf' flag set to True."""
        ret = self.__copy__()
        ret.is_not_in_out_vcf = True
        return ret

    def __copy__(self):
        """Creates a shallow copy of the instance."""
        return BcfFormatStruct(self.id, self.in_num_1, self.out_num_2, self.type, self.description)

BCF_STRING = 'BCF_STRING'
BCF_INTEGER = 'BCF_INTEGER'
BCF_NUM_A = 'BCF_NUM_A'
BCF_NUM_R = 'BCF_NUM_R'
BCF_SIG_INT = 'BCF_SIG_INT'
BCF_S64_INT = 'BCF_S64_INT'
BCF_SEP = 'BCF_SEP'

FORMAT_VEC = [
    BcfFormatStruct("GT", 1, BCF_STRING, "Genotype (for tumor cells, this is only a guess)"),
    BcfFormatStruct("GQ", 1, BCF_INTEGER, "Genotype Quality."),
    BcfFormatStruct("HQ", 2, BCF_INTEGER, "Haplotype Quality."),
    BcfFormatStruct("FT", 1, BCF_STRING, "Sample genotype filter indicating if this genotype was 'called' (similar in concept to the FILTER field). "
                                        "Again, use PASS to indicate that all filters have been passed, a semi-colon separated list of codes for filters "
                                        "that fail, or ‘.’ to indicate that filters have not been applied. "
                                        "These values should be described in the meta-information in the same way as FILTERs (String, no white-space or semi-colons permitted)"),
    BcfFormatStruct("FTS", 'A', BCF_STRING, "Sample variant filter indicating if this variant was 'called' (similar in concept to the FILTER field). "
                                           "Again, use PASS to indicate that all filters have been passed, "
                                           "a vertical bar (|)-separated list of codes for filters that fail, "
                                           "or '.' to indicate that filters have not been applied. "
                                           "These values should be described in the meta-information in the same way as FILTERs. "
                                           "No white-space, semi-colons, or vertical bar (|) permitted."),
    
    BcfFormatStruct("_A_", 1, BCF_SEP, "Summary statistics."),
    BcfFormatStruct("DP", 1, BCF_INTEGER, "Fragment depth of coverage with duplicates removed."),
    BcfFormatStruct("AD", 'R', BCF_INTEGER, "Fragment depth supporting the ALT allele with duplicates removed."),
    BcfFormatStruct("bDP", 1, BCF_INTEGER, "Fragment depth of coverage with duplicates kept."),
    BcfFormatStruct("bAD", 'R', BCF_INTEGER, "Fragment depth supporting the ALT allele with duplicates kept."),
    BcfFormatStruct("c2DP", 1, BCF_INTEGER, "Consensus UMI-barcode family depth of coverage using tier-2 thresholds for grouping fragments into families."),
    BcfFormatStruct("c2AD", 'R', BCF_INTEGER, "Consensus UMI_barcode family depth of coverage supporting the ALT allele using tier-2 thresholds for grouping fragments into families."),
    
    BcfFormatStruct("_Aa", 1, BCF_SEP, "Preparation statistics for segment biases at this position."),
    BcfFormatStruct("APDP", [1, 4, 4, 2, 1], BCF_INTEGER, "Read segment sequencing depths with the following characteristics: total (1), "
                                                        "within the InDel length of insertion (2) and deletion (3), "
                                                        "within the tandem-repeat track length of insertion (4) and deletion (5), "
                                                        "originated from PCR amplicons (6), of SNV (7), of DNV (8), "
                                                        "of high quality (9), "
                                                        "near-clip (10), supported by confident alignments which have no long InDels and no long clips (11), "
                                                        "and UMI (unique molecular identifier, a.k.a. molecular barcode)-labeled (12)."),
    BcfFormatStruct("APXM", [4, 3, 1], BCF_S64_INT, "Expected number of mismatches (1) and gap openings (2) in a 1500-bp window. "
                                                  "Total sum of query length (3). Total sum of average InDel length of each sequenced segment (4). "
                                                  "The (sum of squares (5,6)) and (sum of 100 divided by (7,8)) of insertion (5,7) and deletion (6,8) lengths."),
    
    BcfFormatStruct("_Ab", 1, BCF_SEP, "Preparation statistics for segment biases at this position."),
    BcfFormatStruct("APLRID", 4, BCF_S64_INT, "Summed squared insertion (1,2) and deletion (3,4) lengths to the left (1,3) and right (2,4) ends of the InDel-affected region."),
    BcfFormatStruct("APLRI", 4, BCF_S64_INT, "Summed distance to left insert end and the number of such inserts, and similarly for right insert end."),
    BcfFormatStruct("APLRP", 4, BCF_INTEGER, "Summed distance to left and right ends, summed insertion length, and summed deletion length."),
    
    BcfFormatStruct("_Ac", 1, BCF_SEP, "Threshold for each type of bias (tier-1 means weak bias and tier-2 means strong bias)."),

    # Compiler conditionals
    # if COMPILATION_TRY_HIGH_DEPTH_POS_BIAS
    #     BcfFormatStruct("APPB", [4, 4], BCF_INTEGER, "Preparation statistics for position bias."),
    # end if

    # if COMPILATION_ENABLE_XMGOT
    #     BcfFormatStruct("AXMT", 2, BCF_INTEGER, "Number of mismatches on read-segment above which there is tier-1 and tier-2 mismatch bias."),
    # end if

    BcfFormatStruct("ALRPxT", 2, BCF_INTEGER, "Number of bases to left (1,2) and right (3,4) segment ends above which the segment is not used for computing position bias."),
    BcfFormatStruct("ALRIT", 4, BCF_INTEGER, "Number of bases to left (1,2) and right (3,4) insert ends above which there is tier-1 and tier-2 insert bias."),
    BcfFormatStruct("ALRIt", 4, BCF_INTEGER, "Number of bases to left (1,2) and right (3,4) insert ends below which there is tier-1 and tier-2 insert bias."),
    BcfFormatStruct("ALRPt", 4, BCF_INTEGER, "Number of bases to left (1,2) and right (3,4) read-segment ends below which there is tier-1 and tier-2 position bias."),
    BcfFormatStruct("ALRBt", 4, BCF_INTEGER, "Base alignment quality (BAQ) to left (1,2) and right (3,4) read-segment ends below which there is tier-1 and tier-2 position bias."),
    BcfFormatStruct("_AQ"   , 1,         BCF_SEP,     "Sum of qualities "
                                         "(For FORMAT/TAG with the prefixes '_A', '_B', '_C', or '_D' in the SUB-HEADER without checking whether the first letter is in upper or lower case, "
                                         "the TAG values are for REF/ALT if Number=R (i.e., starting with the letter A, B, C or D), "
                                         "all alleles by sum if Number=1 (i.e., starting with the letter a, b, c or d), "
                                         "and all-alleles by sum/the padded deletion allele if Number=2 (i.e., starting with a, b, c or d)). "
                                         "The f, r, and b letter suffixes mean forward, reverse, and both directions, respectively. "),
    BcfFormatStruct("aMQs"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment sum of mapping qualities for the REF and ALT alleles. "),
    BcfFormatStruct("AMQs"  , 2,1,       BCF_INTEGER, "Raw sequencing segment sum of mapping qualities for all alleles by sum and the padded deletion. "),
    BcfFormatStruct("a1BQf" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing-segment sum of base quality on the forward strand. "),
    BcfFormatStruct("A1BQf" , 2,1,       BCF_INTEGER, "Raw sequencing-segment sum of base quality on the forward strand. "),
    BcfFormatStruct("a1BQr" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing-segment sum of base quality on the reverse strand. "),
    BcfFormatStruct("A1BQr" , 2,1,       BCF_INTEGER, "Raw sequencing-segment sum of base quality on the reverse strand. "),
    
    BcfFormatStruct("_ADPf" , 1,         BCF_SEP,     "Raw sequencing segment depths with forward orientation. "),
    BcfFormatStruct("aDPff" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth with the R1-forward orientation and strand. "),
    BcfFormatStruct("ADPff" , 2,         BCF_INTEGER, "Raw sequencing segment depth with the R1-forward orientation and strand. "),
    BcfFormatStruct("aDPfr" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth with the R2-reverse orientation and strand. "),
    BcfFormatStruct("ADPfr" , 2,         BCF_INTEGER, "Raw sequencing segment depth with the R2-reverse orientation and strand. "),
    
    BcfFormatStruct("_ADPr" , 1,         BCF_SEP,     "Raw sequencing segment depths with reverse orientation. "),
    BcfFormatStruct("aDPrf" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth with the R2-forward orientation and strand. "),
    BcfFormatStruct("ADPrf" , 2,         BCF_INTEGER, "Raw sequencing segment depth with the R2-forward orientation and strand. "),
    BcfFormatStruct("aDPrr" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth with the R1-reverse orientation and strand. "),
    BcfFormatStruct("ADPrr" , 2,         BCF_INTEGER, "Raw sequencing segment depth with the R1-reverse orientation and strand. "),

    BcfFormatStruct("_ALP"  , 1,         BCF_SEP,     "Raw sequencing segment statistics related to position bias on the left side. "),
    BcfFormatStruct("aLP1"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 left-side position bias. "),
    BcfFormatStruct("ALP1"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 left-side position bias. "),
    BcfFormatStruct("aLP2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 left-side position bias. "),
    BcfFormatStruct("ALP2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 left-side position bias. "),
    BcfFormatStruct("aLPL"  , BCF_NUM_R, BCF_S64_INT, "Raw summed distance (number of bases) to the left-side sequencing-segment end using only high-quality bases far from alignment ends. "),
    BcfFormatStruct("ALPL"  , 2,1,       BCF_S64_INT, "Raw summed distance (number of bases) to the left-side sequencing-segment end using only high-quality bases far from alignment ends. "),
    
    BcfFormatStruct("_ARP"  , 1,         BCF_SEP,     "Raw sequencing segment statistics related to position bias on the right side. "),
    BcfFormatStruct("aRP1"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 right-side position bias. "),
    BcfFormatStruct("ARP1"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 right-side position bias. "),
    BcfFormatStruct("aRP2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 right-side position bias. "),
    BcfFormatStruct("ARP2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 right-side position bias. "),
    BcfFormatStruct("aRPL"  , BCF_NUM_R, BCF_S64_INT, "Raw summed distance (number of bases) to the right-side sequencing-segment end using only high-quality bases far from alignment ends. "),
    BcfFormatStruct("ARPL"  , 2,1,       BCF_S64_INT, "Raw summed distance (number of bases) to the right-side sequencing-segment end using only high-quality bases far from alignment ends. "),

    BcfFormatStruct("_ALB"  , 1,         BCF_SEP,     "Raw sequencing segment statistics related to base-alignment-quality (BAQ) bias on the left side. "),
    BcfFormatStruct("aLB1"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 left-side base-alignment bias. "),
    #BcfFormatStruct("ALB1"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 left-side position bias. "),
    BcfFormatStruct("aLB2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 left-side base-alignment bias. "),
    BcfFormatStruct("ALB2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 left-side position bias. "),
    BcfFormatStruct("aLBL"  , BCF_NUM_R, BCF_S64_INT, "Raw summed BAQ (base-alignment quality) to the left-side sequencing-segment end. "),
    BcfFormatStruct("ALBL"  , 2,1,       BCF_S64_INT, "Raw summed distance (number of bases) to the left-side sequencing-segment end. "),
    
    BcfFormatStruct("_ARB"  , 1,         BCF_SEP,     "Raw sequencing segment statistics related to base-alignment-quality (BAQ) bias on the right side. "),
    BcfFormatStruct("aRB1"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 right-side base-alignment bias. "),
    #BcfFormatStruct("ARB1"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 right-side position bias. "),
    BcfFormatStruct("aRB2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 right-side base-alignment bias. "),
    BcfFormatStruct("ARB2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 right-side position bias. "),
    BcfFormatStruct("aRBL"  , BCF_NUM_R, BCF_S64_INT, "Raw summed BAQ (base-alignment quality) to the right-side sequencing-segment end. "),
    BcfFormatStruct("ARBL"  , 2,1,       BCF_S64_INT, "Raw summed distance (number of bases) to the right-side sequencing-segment end. "),

    BcfFormatStruct("_ALI"  , 1,         BCF_SEP,     "Raw sequencing segment statistics related to insert-end bias on the left side. "),
    BcfFormatStruct("aLI1"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 insert bias on the left side. "),
    #BcfFormatStruct("ALI1"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 insert bias on the left side. "),
    BcfFormatStruct("aLI2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 insert bias on the left side. "),
    BcfFormatStruct("ALI2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 insert bias on the left side. "),
    BcfFormatStruct("aLIr"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth eligible for left-side reverse-strand bias computation. "),
    BcfFormatStruct("ALIr"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth eligible for left-side reverse-strand bias computation. "),

    BcfFormatStruct("_ARI"  , 1,         BCF_SEP,     "Raw sequencing segment statistics related to insert-end bias on the right side. "),
    BcfFormatStruct("aRI1"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 insert bias on the right side. "),
    #BcfFormatStruct("ARI1"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 insert bias on the right side. "),
    BcfFormatStruct("aRI2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 insert bias on the right side. "),
    BcfFormatStruct("ARI2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 insert bias on the right side. "),
    BcfFormatStruct("aRIf"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth eligible for right-side forward-strand bias computation. "),
    BcfFormatStruct("ARIf"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth eligible for right-side forward-strand bias computation. "),
    
    BcfFormatStruct("_AX"   , 1,         BCF_SEP,     "Raw sequencing segment statistics for extra information. "),
    BcfFormatStruct("aBQ2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 base quality bias. "),
    BcfFormatStruct("ABQ2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 base quality bias. "),
    #BcfFormatStruct("APF1"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 mismatch bias. "),
    BcfFormatStruct("aPF2"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 relative mismatch bias and base quality bias. "),
    BcfFormatStruct("APF2"  , 2,1,       BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-2 mismatch bias. "),
    BcfFormatStruct("aP1"   , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth of reads passing left and right number of bases threshold of distance. "),
    BcfFormatStruct("AP1"   , 2,1,       BCF_INTEGER, "Raw sequencing segment depth of reads passing left and right number of bases threshold of distance. "),
    BcfFormatStruct("aP2"   , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth of reads that are either labeled with UMIs or not coming from PCR amplicons. "),
    BcfFormatStruct("AP2"   , 2,1,       BCF_INTEGER, "Raw sequencing segment depth of reads that are either labeled with UMIs or not coming from PCR amplicons. "),

    BcfFormatStruct("_Ax"   , 1,         BCF_SEP,     "Raw sequencing segment statistics for extra information for only the REF and ALT alleles. "),
    BcfFormatStruct("aPF1"  , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by tier-1 relative mismatch bias and base quality bias. "),
    #BcfFormatStruct("aLPT"  , BCF_NUM_R, BCF_INTEGER, "Raw summed distance (number of bases) to the left-side sequencing-segment end. "),
    #BcfFormatStruct("aRPT"  , BCF_NUM_R, BCF_INTEGER, "Raw summed distance (number of bases) to the right-side sequencing-segment end. "),
    BcfFormatStruct("aLIT"  , BCF_NUM_R, BCF_S64_INT, "Raw summed distance (number of bases) to the left-side insert end. "),
    BcfFormatStruct("aRIT"  , BCF_NUM_R, BCF_S64_INT, "Raw summed distance (number of bases) to the right-side insert end. "),
    BcfFormatStruct("aP3"   , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth of reads that are not affected by nearby InDels. "),
    BcfFormatStruct("aNC"   , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth of reads that do not have any clips (including soft and hard clips). "),
    
    BcfFormatStruct("_BDP"  , 1,         BCF_SEP,     "Non-de-duplicated fragment depth for all alleles by sum and the padded deletion allele. "),
    BcfFormatStruct("bDPf"  , BCF_NUM_R, BCF_INTEGER, "See BDPf. "),
    # BcfFormatStruct("BDPf"  , 2,         BCF_INTEGER, "Non-de-duplicated fragment depth on the forward strand for all alleles by sum and the padded deletion allele. "),
    BcfFormatStruct("bDPr"  , BCF_NUM_R, BCF_INTEGER, "See BDPr. "),
    # BcfFormatStruct("BDPr"  , 2,         BCF_INTEGER, "Non-de-duplicated fragment depth on the reverse strand for all alleles by sum and the padded deletion allele. "),
    BcfFormatStruct("BDPb"  , 2,         BCF_INTEGER, "Non-de-duplicated fragment depth on the forward and reverse strands for all alleles by sum. "),
    BcfFormatStruct("BDPd"  , 2,         BCF_INTEGER, "Non-de-duplicated fragment depth on the forward and reverse strands for the padded deletion allele. "),
    
    # BcfFormatStruct("_BT"   , 1,         BCF_SEP,     "Non-de-duplicated fragment depth for all alleles by sum and the padded deletion allele. "),
    BcfFormatStruct("bTAf"  , BCF_NUM_R, BCF_INTEGER, "See BTAf. "),
    # BcfFormatStruct("BTAf"  , 2,1,       BCF_INTEGER, "Non-de-duplicated sum of sequenced fragment positions on the forward strand for all alleles by sum. "),
    BcfFormatStruct("bTAr"  , BCF_NUM_R, BCF_INTEGER, "See BTAr. "),
    # BcfFormatStruct("BTAr"  , 2,1,       BCF_INTEGER, "Non-de-duplicated sum of sequenced fragment positions on the reverse strand for all alleles by sum. "),
    BcfFormatStruct("BTAb"  , 2,         BCF_INTEGER, "Non-de-duplicated sum of sequenced fragment positions on the forward and reverse strands for all alleles by sum. "),
    
    BcfFormatStruct("bTBf"  , BCF_NUM_R, BCF_INTEGER, "See BTBf. "),
    # BcfFormatStruct("BTBf"  , 2,1,       BCF_INTEGER, "Non-de-duplicated sum of sequenced fragment positions near mutations on the forward strand for all alleles by sum. "),
    BcfFormatStruct("bTBr"  , BCF_NUM_R, BCF_INTEGER, "See BTBr. "),
    # BcfFormatStruct("BTBr"  , 2,1,       BCF_INTEGER, "Non-de-duplicated sum of sequenced fragment positions near mutations on the reverse strand for all alleles by sum. "),
    BcfFormatStruct("BTBb"  , 2,         BCF_INTEGER, "Non-de-duplicated sum of sequenced fragment positions near mutations on the forward and reverse strands for all alleles by sum. "),
    
    BcfFormatStruct("_CDP1" , 1,         BCF_SEP,     "De-duplicated depths of the unique molecular fragments for all alleles by sum and the padded deletion allele. "),
    BcfFormatStruct("cDP1f" , BCF_NUM_R, BCF_INTEGER, "Non-filtered de-duplicated depth of the unique molecular fragments on the forward read orientation. "),
    #BcfFormatStruct("CDP1f" , 2,         BCF_INTEGER, "Non-filtered de-duplicated depth of the unique molecular fragments on the forward read orientation. "),
    BcfFormatStruct("cDP1r" , BCF_NUM_R, BCF_INTEGER, "Non-filtered de-duplicated depth of the unique molecular fragments on the reverse read orientation. "),
   # BcfFormatStruct("CDP1r" , 2,         BCF_INTEGER, "Non-filtered de-duplicated depth of the unique molecular fragments on the reverse read orientation. "),
    BcfFormatStruct("CDP1b" , 2,         BCF_INTEGER, "Non-filtered de-duplicated depth of the unique molecular fragments on the forward and reverse read orientations for all alleles by sum. "),
    BcfFormatStruct("CDP1d" , 2,         BCF_INTEGER, "Non-filtered de-duplicated depth of the unique molecular fragments on the forward and reverse read orientations for the padded deletion allele. "),

    BcfFormatStruct("cDP12f", BCF_NUM_R, BCF_INTEGER, "BQ-filtered de-duplicated depth of the unique molecular fragments on the forward read orientation. "),
    # BcfFormatStruct("CDP12f", 2,         BCF_INTEGER, "BQ-filtered de-duplicated depth of the unique molecular fragments on the forward read orientation . "),
    BcfFormatStruct("cDP12r", BCF_NUM_R, BCF_INTEGER, "BQ-filtered de-duplicated depth of the unique molecular fragments on the reverse read orientation. "),
    # BcfFormatStruct("CDP12r", 2,         BCF_INTEGER, "BQ-Filtered de-duplicated depth of the unique molecular fragments on the reverse read orientation. "),
    BcfFormatStruct("CDP12b", 2,         BCF_INTEGER, "BQ-Filtered de-duplicated depth of the unique molecular fragments on the forward and reverse read orientations. "),
    
    BcfFormatStruct("_CDP2" , 1,         BCF_SEP,     "Tier-2 single-strand consensus sequence (SSCS) depth. "),
    BcfFormatStruct("cDP2f" , BCF_NUM_R, BCF_INTEGER, "SSCS depth on the forward read orientation for each allele. "),
    # BcfFormatStruct("CDP2f" , 2,         BCF_INTEGER, "SSCS depth on the forward read orientation for all alleles by sum. "),
    BcfFormatStruct("cDP2r" , BCF_NUM_R, BCF_INTEGER, "SSCS depth on the reverse read orientation for each allele. "), 
    # BcfFormatStruct("CDP2r" , 2,         BCF_INTEGER, "SSCS depth on the reverse read orientation for all alleles by sum. "),
    BcfFormatStruct("CDP2b" , 2,         BCF_INTEGER, "SSCS depth on the forward and reverse read orientations for all alleles by sum. "),
    BcfFormatStruct("CDP2d" , 2,         BCF_INTEGER, "SSCS depth on the forward and reverse read orientations for the padded deletion allele. "),

    BcfFormatStruct("c2BQ2" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-2 base quality bias. ").sscs(),
    BcfFormatStruct("C2BQ2" , 2,1,       BCF_INTEGER, "SSCS depth unaffected by tier-2 base quality bias. ").sscs(),
    
    BcfFormatStruct("c2LP0" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by strictly defined no-prior left-side position bias. ").sscs(),
    BcfFormatStruct("C2LP0" , 2,1,       BCF_INTEGER, "SSCS depth unaffected by strictly defined no-prior left-side position bias. ").sscs(),
    BcfFormatStruct("c2RP0" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by strictly defined no-prior right-side position bias. ").sscs(),
    BcfFormatStruct("C2RP0" , 2,1,       BCF_INTEGER, "SSCS depth unaffected by strictly defined no-prior right-side position bias. ").sscs(),
    
    BcfFormatStruct("_C2XP" , 1,         BCF_SEP,     "SSCS statistics related to position bias. "
                                         "If this tag is present and absent, then all SSCS-related tags are all present and absent, respectively. ").sscs(),
    BcfFormatStruct("c2LP1" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-1 left-side position bias. ").sscs(),
    BcfFormatStruct("c2LP2" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-2 left-side position bias. ").sscs(),
    BcfFormatStruct("C2LP2" , 2,1,       BCF_INTEGER, "SSCS depth unaffected by tier-2 left-side position bias. ").sscs().not_put_in_vcf(),    
    BcfFormatStruct("c2RP1" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-1 right-side position bias. ").sscs(),
    BcfFormatStruct("c2RP2" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-2 right-side position bias. ").sscs(),
    BcfFormatStruct("C2RP2" , 2,1,       BCF_INTEGER, "SSCS depth unaffected by tier-2 right-side position bias. ").sscs().not_put_in_vcf(),
    BcfFormatStruct("c2LPL" , BCF_NUM_R, BCF_S64_INT, "Raw summed distance (number of bases) to the left-side tier-2 SSCS end. ").sscs(),
    BcfFormatStruct("C2LPL" , 2,1,       BCF_S64_INT, "Raw summed distance (number of bases) to the left-side tier-2 SSCS end. ").sscs().not_put_in_vcf(),
    BcfFormatStruct("c2RPL" , BCF_NUM_R, BCF_S64_INT, "Raw summed distance (number of bases) to the right-side tier-2 SSCS end. ").sscs(),
    BcfFormatStruct("C2RPL" , 2,1,       BCF_S64_INT, "Raw summed distance (number of bases) to the right-side tier-2 SSCS end. ").sscs().not_put_in_vcf(),
    
    BcfFormatStruct("_C2XB" , 1,         BCF_SEP,     "SSCS statistics related to alignment quality bias. ").sscs(),
    BcfFormatStruct("c2LB1" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-1 left-side base-alignment bias. ").sscs(),
    BcfFormatStruct("c2LB2" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-2 left-side base-alignment bias. ").sscs(),
    BcfFormatStruct("C2LB2" , 2,1,       BCF_INTEGER, "SSCS depth unaffected by tier-2 left-side position bias. ").sscs().not_put_in_vcf(),
    BcfFormatStruct("c2RB1" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-1 right-side base-alignment bias. ").sscs(),
    BcfFormatStruct("c2RB2" , BCF_NUM_R, BCF_INTEGER, "SSCS depth unaffected by tier-2 right-side base-alignment bias. ").sscs(),
    BcfFormatStruct("C2RB2" , 2,1,       BCF_INTEGER, "SSCS depth unaffected by tier-2 right-side position bias. ").sscs().not_put_in_vcf(),
    BcfFormatStruct("c2LBL" , BCF_NUM_R, BCF_S64_INT, "Raw summed BAQ (base-alignment quality) to the left-side of tier-2 SSCS. ").sscs(),
    BcfFormatStruct("C2LBL" , 2,1,       BCF_S64_INT, "Raw summed BAQ (base-alignment quality) to the left-side of tier-2 SSCS. ").sscs().not_put_in_vcf(),
    BcfFormatStruct("c2RBL" , BCF_NUM_R, BCF_S64_INT, "Raw summed BAQ (base-alignment quality) to the left-side of tier-2 SSCS. ").sscs(), 
    BcfFormatStruct("C2RBL" , 2,1,       BCF_S64_INT, "Raw summed BAQ (base-alignment quality) to the left-side of tier-2 SSCS. ").sscs().not_put_in_vcf(),
    
    BcfFormatStruct("_CDPx" , 1,         BCF_SEP,     "Other extra tags extracted from single-strand consensus sequences (SSCSs) derived by UMI molecular-barcode families. ").sscs(),
    BcfFormatStruct("cDP3f" , BCF_NUM_R, BCF_INTEGER, "Strong SSCS depth on the forward read orientation for each allele. ").sscs(),
    #/ BcfFormatStruct("CDP3f" , 2,1,       BCF_INTEGER, "Strong SSCS depth on the forward read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("cDP3r" , BCF_NUM_R, BCF_INTEGER, "Strong SSCS depth on the reverse read orientation for each allele. ").sscs(),
    # BcfFormatStruct("CDP3r" , 2,1,       BCF_INTEGER, "Strong SSCS depth on the reverse read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("CDP3b" , 2,         BCF_INTEGER, "Strong SSCS depth on the forward and reverse read orientations for all alleles by sum. ").sscs(),
    
    BcfFormatStruct("cDP21f", BCF_NUM_R, BCF_INTEGER, "SSCS singleton on the forward read orientation. ").sscs(),
    #BcfFormatStruct("CDP21f", 2,1,       BCF_INTEGER, "SSCS singleton on the forward read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("cDP21r", BCF_NUM_R, BCF_INTEGER, "SSCS singleton on the reverse read orientation. ").sscs(),
    #BcfFormatStruct("CDP21r", 2,1,       BCF_INTEGER, "SSCS singleton on the reverse read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("CDP21b" , 2,         BCF_INTEGER, "SSCS singleton on the forward and reverse read orientations for all alleles by sum. ").sscs(),
    
    BcfFormatStruct("_cDPMm", 1,         BCF_SEP,     "Empirical PCR-fragment (with dups) error in SSCS UMI-families used to estimate base-call-like qualities. ").sscs(),
    BcfFormatStruct("cDPMf" , BCF_NUM_R, BCF_INTEGER, "Depth of PCR fragments supporting the UMI-consensus allele on the forward read orientation for each allele. ").sscs(),
    # BcfFormatStruct("CDPMf" , 2,1,       BCF_INTEGER, "Depth of PCR fragments supporting the UMI-consensus allele on the forward read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("cDPMr" , BCF_NUM_R, BCF_INTEGER, "Depth of PCR fragments supporting the UMI-consensus allele on the reverse read orientation for each allele. ").sscs(),
    # BcfFormatStruct("CDPMr" , 2,1,       BCF_INTEGER, "Depth of PCR fragments supporting the UMI-consensus allele on the reverse read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("CDPMb"  , 2,         BCF_INTEGER, "Depth of PCR fragments supporting the UMI-consensus allele on the forward and reverse read orientations for all alleles by sum. ").sscs(),
    BcfFormatStruct("cDPmf" , BCF_NUM_R, BCF_INTEGER, "Depth of PCR fragments not supporting the UMI-consensus allele on the forward read orientation for each allele. ").sscs(),
    # BcfFormatStruct("CDPmf" , 2,1,       BCF_INTEGER, "Depth of PCR fragments not supporting the UMI-consensus allele on the forward read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("cDPmr" , BCF_NUM_R, BCF_INTEGER, "Depth of PCR fragments not supporting the UMI-consensus allele on the reverse read orientation for each allele. ").sscs(),
    # BcfFormatStruct("CDPmr" , 2,1,       BCF_INTEGER, "Depth of PCR fragments not supporting the UMI-consensus allele on the reverse read orientation for all alleles by sum. ").sscs(),
    BcfFormatStruct("CDPmb"  , 2,         BCF_INTEGER, "Depth of PCR fragments not supporting the UMI-consensus allele on the forward and reverse read orientations for all alleles by sum. ").sscs(),
    
    BcfFormatStruct("CDPDb" , 2,         BCF_INTEGER, "DSCS-excluded SSCS depths on the forward and reverse read orientations for all alleles by sum. "),
    BcfFormatStruct("cDPDf" , BCF_NUM_R, BCF_INTEGER, "DSCS-excluded SSCS depth on the forward read orientation. "),
    BcfFormatStruct("cDPDr" , BCF_NUM_R, BCF_INTEGER, "DSCS-excluded SSCS depth on the reverse read orientation. "),
    
    BcfFormatStruct("_DDP"  , 1,         BCF_SEP,     "Duplex consensus sequence (DCS, or double-strand consensus sequence (DSCS)) depths from the original double-stranded input molecule. "),
    BcfFormatStruct("DDP1"  , 2,         BCF_INTEGER, "DCS depth regardless of allele agreement on the two strands for all alleles by sum and the padded deletion allele. "),
    BcfFormatStruct("dDP1"  , BCF_NUM_R, BCF_INTEGER, "DCS depth regardless of allele agreement on the two strands for each allele. "),
    BcfFormatStruct("DDP2"  , 2,         BCF_INTEGER, "DCS depth with allele agreement on the two strands for all alleles by sum and the padded deletion allele. "),
    BcfFormatStruct("dDP2"  , BCF_NUM_R, BCF_INTEGER, "DCS depth with allele agreement on the two strands for each allele. "),
    
    BcfFormatStruct("_ea"   , 1,         BCF_SEP,     "Error variables inferred from systematically low base-call qualities (BQs). "),
    BcfFormatStruct("aBQ"   , BCF_NUM_R, BCF_SIG_INT, "Root-mean-square base quality for sequencing segments. "),
    BcfFormatStruct("a2BQf" , BCF_NUM_R, BCF_INTEGER, "Summed squared/32 sequencing-segment base quality on the forward strand. "),
    BcfFormatStruct("a2BQr" , BCF_NUM_R, BCF_INTEGER, "Summed squared/32 sequencing-segment base quality on the reverse strand. "),
    BcfFormatStruct("a2XM2" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by absolute mismatch bias. "),
    BcfFormatStruct("a2BM2" , BCF_NUM_R, BCF_INTEGER, "Raw sequencing segment depth unaffected by absolute base-specific mismatch bias. "),
    BcfFormatStruct("aBQQ"  , BCF_NUM_R, BCF_SIG_INT, "Variant quality capped by systematic error inferred from base qualities. "),    

    BcfFormatStruct("_eb"   , 1,         BCF_SEP,     "Error variables inferred from systematically low mapping qualities (MAPQs or MQs). "),
    BcfFormatStruct("bMQ"   , BCF_NUM_R, BCF_SIG_INT, "Root-mean-square mapping quality for read fragments (max of R1 and R2 MQ is taken). "),
    BcfFormatStruct("aAaMQ" , BCF_NUM_R, BCF_SIG_INT, "Read segment difference of average mapping quality between the ALT allele and the non-ALT alleles. "),
    BcfFormatStruct("bNMQ"  , BCF_NUM_R, BCF_INTEGER, "Phred penalty inferred from high-BQ mismatches to the mapping quality (MAPQ). "
                    "This penalty increases the MAPQ-related systematic error. "),
    BcfFormatStruct("bNMa"  , BCF_NUM_R, BCF_INTEGER, "Percent of the number of fragment positions that are affected by nearby high-BQ mutation "
                    "(by default, nearby means within one turn of DNA helix) for the ALT alleles. "),
    BcfFormatStruct("bNMb"  , BCF_NUM_R, BCF_INTEGER, "Percent of the number of fragment positions that are affected by nearby high-BQ mutation "
                    "(by default, nearby means within one turn of DNA helix) for all non-ALT alleles. "),
    BcfFormatStruct("bMQQ"  , BCF_NUM_R, BCF_SIG_INT, "Variant quality capped by systematic error inferred from mapping qualities. "),

    BcfFormatStruct("_eB"  , 1,         BCF_SEP,     "Quality-related variables assuming IID read support (IID: independent and identically distributed) for duped reads. "),
    BcfFormatStruct("bIAQb" , BCF_NUM_R, BCF_SIG_INT, "IID allele quality maximized with IAD and IDQ. "),
    BcfFormatStruct("bIADb" , BCF_NUM_R, BCF_INTEGER, "IID allele depth (number of reads supporting each ALT). "),
    BcfFormatStruct("bIDQb" , BCF_NUM_R, BCF_SIG_INT, "IDD quality threshold per read support. "),
    
    BcfFormatStruct("_eC"  , 1,         BCF_SEP,     "Quality-related variables assuming read supports are IID for de-duplicated reads. "),
    BcfFormatStruct("cIAQf" , BCF_NUM_R, BCF_SIG_INT, "IID allele quality maximized with IAD and IDQ on the forward read orientation. "),
    BcfFormatStruct("cIADf" , BCF_NUM_R, BCF_INTEGER, "IID allele depth (number of reads supporting each ALT) on the forward read orientation. "),
    BcfFormatStruct("cIDQf" , BCF_NUM_R, BCF_SIG_INT, "IDD quality threshold per read support on the forward read orientation. "),
    
    BcfFormatStruct("cIAQr" , BCF_NUM_R, BCF_SIG_INT, "IID allele quality maximized with IAD and IDQ on the reverse read orientation. "),
    BcfFormatStruct("cIADr" , BCF_NUM_R, BCF_INTEGER, "IID allele depth (number of reads supporting each ALT) on the reverse read orientation. "),
    BcfFormatStruct("cIDQr" , BCF_NUM_R, BCF_SIG_INT, "IDD quality threshold per read support on the reverse read orientation. "),
    
    BcfFormatStruct("_eE"  , 1,         BCF_SEP,     "Binomial variant qualities. "),
    BcfFormatStruct("bIAQ"  , BCF_NUM_R, BCF_SIG_INT, "The duped fragment binomial variant quality by assuming statistical independence. "),
    BcfFormatStruct("cIAQ"  , BCF_NUM_R, BCF_SIG_INT, "The de-duplicated fragment binomial variant quality by assuming statistical independence. "),
    BcfFormatStruct("bTINQ" , BCF_NUM_R, BCF_SIG_INT, "The fragment binomial tumor-in-normal quality by assuming statistical independence. "),
    BcfFormatStruct("cTINQ" , BCF_NUM_R, BCF_SIG_INT, "The single-strand-consensus-sequence binomial tumor-in-normal quality by assuming statistical independence. "),
 
    BcfFormatStruct("_eQ1"   , 1,         BCF_SEP,     "Power-law variant quality statistics for de-duplicated read fragments. "),
    BcfFormatStruct("cPCQ1" , BCF_NUM_R, BCF_SIG_INT, "The de-duplicated read fragment power-law variant allele quality cap that is not lowered by using matched normal. "),
    BcfFormatStruct("cPLQ1" , BCF_NUM_R, BCF_SIG_INT, "The de-duplicated read fragment power-law variant allele quality. "),
    BcfFormatStruct("cVQ1"  , BCF_NUM_R, BCF_SIG_INT, "The final variant quality computed with de-duplicated read fragments. "),
    BcfFormatStruct("gVQ1"  , BCF_NUM_R, BCF_SIG_INT, "The final variant quality computed with de-duplicated read fragments used for germline variant calls. "),

    BcfFormatStruct("_eQ2"  , 1,         BCF_SEP,     "Power-law variant quality statistics for SSCS UMI-barcoded families. "),
    BcfFormatStruct("cPCQ2" , BCF_NUM_R, BCF_SIG_INT, "The SSCS power-law variant allele quality cap that is not lowered by using matched normal. "),
    BcfFormatStruct("cPLQ2" , BCF_NUM_R, BCF_SIG_INT, "The single-strand-consensus-sequence (SSCS) UMI-barcoded power-law variant allele quality. "),
    BcfFormatStruct("cVQ2"  , BCF_NUM_R, BCF_SIG_INT, "The final variant allele quality computed with SSCS UMI-barcoded families. "),
    BcfFormatStruct("cMmQ"  , BCF_NUM_R, BCF_INTEGER, "The empirical base quality estimated with high-quality UMI barcode families. "
                                                      "This field is defined to be the Phred-scaled fraction of minor read support "
                                                      "to the sum of major and major read support, "
                                                       "where major means agreement with UMI consensus, and minor means disagreement with UMI consensus. "),
    BcfFormatStruct("dVQinc", BCF_NUM_R, BCF_SIG_INT, "The increase in cVQ2 (excluding systematic error) contributed by "
                                                      "double-strand-consensus-sequences (DSCSs) of duplex barcode famillies. "
                                                      "Negative value means no increase. "),
    
    BcfFormatStruct("_CDP1vx", 1,        BCF_SEP,     "Effective read support for de-duplicated fragments. "),
    BcfFormatStruct("cDP1v" , BCF_NUM_R, BCF_INTEGER, "The effective number of de-duplicated read fragments supporting each allele multiplied by 100 "
                                                      "for within-sample comparison. "),
    BcfFormatStruct("CDP1v" , 2,         BCF_INTEGER, "The effective number of de-duplicated read fragments supporting all alleles multiplied by 100 "
                                                      "for within-sample comparison. "),
    BcfFormatStruct("cDP1w" , BCF_NUM_R, BCF_INTEGER, "The effective number of de-duplicated read fragments supporting each allele multiplied by 100 "
                                                      "for sample-specific variant-quality cap. "),
    BcfFormatStruct("CDP1w" , 2,1,       BCF_INTEGER, "The effective number of de-duplicated read fragments supporting all alleles multiplied by 100 "
                                                      "for sample-specific variant-quality cap. "), 
    BcfFormatStruct("cDP1x" , BCF_NUM_R, BCF_INTEGER, "The effective number of de-duplicated read fragments supporting each allele multiplied by 100 "
                                                      "for between-sample comparison. "),
    BcfFormatStruct("CDP1x" , 2,1,       BCF_INTEGER, "The effective number of de-duplicated read fragments supporting all alleles multiplied by 100 "),

    BcfFormatStruct("_CDP2vx", 1,        BCF_SEP,     "Effective read support for single-strand consensus sequence (SSCS) UMI-barcoded families. "),
    BcfFormatStruct("cDP2v" , BCF_NUM_R, BCF_INTEGER, "The effective number of SSCS UMI-barcoded families supporting each allele multiplied by 100 "
                                                      "for within-sample comparison. "),
    BcfFormatStruct("CDP2v" , 2,         BCF_INTEGER, "The effective number of SSCS UMI-barcoded families supporting all alleles multiplied by 100 "
                                                      "for within-sample comparison. "),
    BcfFormatStruct("cDP2w" , BCF_NUM_R, BCF_INTEGER, "The effective number of SSCS UMI-barcoded families supporting each allele multiplied by 100 "
                                                     "for sample-specific variant-quality cap. "),
    BcfFormatStruct("CDP2w" , 2,1,       BCF_INTEGER, "The effective number of SSCS UMI-barcoded families supporting all alleles multiplied by 100 "
                                                      "for sample-specific variant-quality cap. "), 
    BcfFormatStruct("cDP2x" , BCF_NUM_R, BCF_INTEGER, "The effective number of SSCS UMI-barcoded families supporting each allele multiplied by 100 "
                                                     "for between-sample comparison. "),
    BcfFormatStruct("CDP2x" , 2,1,       BCF_INTEGER, "The effective number of SSCS UMI-barcoded families supporting all alleles multiplied by 100 "
                                                      "for between-sample comparison. "),
    
    BcfFormatStruct("_f1"   , 1,         BCF_SEP,     "Filter-related information including counter-filters that rescue variants. "),
    BcfFormatStruct("CONTQ" , BCF_NUM_R, BCF_SIG_INT, "Likelihood of the variant signal if the variant signal is contaminated. "
                                                      "This value rescues variants in the matched normal control sample. "),
    BcfFormatStruct("nPF"   , BCF_NUM_D, BCF_SIG_INT, "Phred prior bias probability for base position and BAQ. "),
    BcfFormatStruct("nNFA"  , BCF_NUM_D, BCF_SIG_INT, "DeciPhred allele fractions computed using nullified bias (meaning that bias in ALT is countered by bias in REF). "),
    BcfFormatStruct("nAFA"  , BCF_NUM_D, BCF_SIG_INT, "DeciPhred allele fractions computed with sequencing-segment depths, "
            "reduced by none, left base position, base right position, left BAQ, right BAQ, left insert position, right insert position, strand, and passing-filter biases (8 biases), respectively. "),
    BcfFormatStruct("nBCFA",  BCF_NUM_D, BCF_SIG_INT, "DeciPhred allele fractions computed with duped and de-duplicated depths, "
            "using duped depth, de-duplicated depth, tier-2 consensus family depth, tier-3 consensus family depth, tier-1 read-orientation depth, and tier-2 read-orientation depth, respectively. "),
    
    BcfFormatStruct("_g1"   , 1,         BCF_SEP,     "General variant-related information. "),
    BcfFormatStruct("VTI"   , BCF_NUM_R, BCF_INTEGER, "Variant-type ID of each allele. "),
    BcfFormatStruct("VTD"   , BCF_NUM_R, BCF_STRING,  "Variant-type description of each allele. "),
    BcfFormatStruct("cVQ1M" , 2,         BCF_SIG_INT, "Consensus allele qualities for de-duplicated fragments and UMI families. "),
    BcfFormatStruct("cVQ2M" , 2,         BCF_SIG_INT, "Consensus allele qualities for de-duplicated fragments and UMI families. "),
    BcfFormatStruct("cVQAM" , 2,         BCF_STRING,  "Consensus allele symbolic descriptions for de-duplicated fragments and UMI families. "),
    BcfFormatStruct("cVQSM" , 2,         BCF_STRING,  "Consensus allele InDel strings for de-duplicated fragments and UMI families. "),
    
    BcfFormatStruct("_g2"    , 1,        BCF_SEP,     "Gap-related information for all observed InDel signals. "), 
    BcfFormatStruct("gapNf"  ,BCF_NUM_D, BCF_INTEGER, "Number of InDel sequences on the forward read orientation. "),
    BcfFormatStruct("gapNr"  ,BCF_NUM_D, BCF_INTEGER, "Number of InDel sequences on the reverse read orientation. "),
    BcfFormatStruct("gapSeq" ,BCF_NUM_D, BCF_STRING,  "InDel sequences. "),
    BcfFormatStruct("gapbAD1",BCF_NUM_D, BCF_INTEGER, "Duped read count of each gapSeq. "),
    BcfFormatStruct("gapcAD1",BCF_NUM_D, BCF_INTEGER, "De-duplicated read count of each gapSeq. "),
    BcfFormatStruct("gc2AD"  ,BCF_NUM_D, BCF_INTEGER, "De-duplicated read count of each gapSeq using tier-2 consensus "
                              "(by default, 0.8 is the consensus allele proportion in family and 2 is the family size). "),
    BcfFormatStruct("gc2dAD", BCF_NUM_D, BCF_INTEGER, "De-duplicated read count of each gapSeq using tier-2 consensus "
                              "with rescue by duplex consensus sequence (DCS) or double-strand consensus sequence (DSC), "
                              "meaning that alpha-beta singleton and beta-alpha singleton are counted as two units of evidence in support of the allele instead of being rejected. "),
    
    BcfFormatStruct("_g3"    , 1,        BCF_SEP,     "Gap-related information for each InDel allele. "),

    BcfFormatStruct("bDPa"   ,BCF_NUM_R, BCF_INTEGER, "Number of non-de-duplicated fragments supporting each ALT allele which is more precise for InDels. "),
    BcfFormatStruct("cDP0a"  ,BCF_NUM_R, BCF_INTEGER, "Number of de-duplicated fragments supporting each ALT allele which is more precise for InDels. "),
    BcfFormatStruct("gapSa"  ,BCF_NUM_R, BCF_STRING,  "InDel string of each allele. "),
    
    BcfFormatStruct("_h1"   , 1,         BCF_SEP,     "Haplotype-related information. "), 
    BcfFormatStruct("bHap"  , 1,         BCF_STRING,  "Duped forward&reverse linkage in the format of "
                                                      "((position&variantType)...forwardHAD&reverseHAD[forwardTotalHAD,reverseTotalHAD])... "
                                                      "where HAD is the haplotype allele depth and "
                                                      "where ()... means more elements following the format in the preceding parenthesis. "),
    BcfFormatStruct("cHap"  , 1,         BCF_STRING,  "Same as bHap except that duplicated reads are counted only once (dedupped). "),
    BcfFormatStruct("c2Hap" , 1,         BCF_STRING,  "Same as cHap except that reads are grouped into UMI barcode families using tier-2 consensus. "),
    
    BcfFormatStruct("_i1"   , 1,         BCF_SEP,     "Other information. "),
    BcfFormatStruct("vHGQ"  , 1,         BCF_INTEGER, "Phred-scaled odds of observing the allele distribution at this genomic position "
                                                      "assuming all alleles were generated by germline events (higher means less likely). "),
    BcfFormatStruct("vAC"   , 2,         BCF_INTEGER,  "Number of SNVs and InDels that passed their variant quality thresholds at this position. This field can be used to filter out multiallelic variants or to merge alleles at the same position. "),
    BcfFormatStruct("vNLODQ", 2,         BCF_SIG_INT,  "Number of SNVs and InDels that passed their variant quality thresholds at this position. This field can be used to filter out SNV-in-tumor with InDel-in-normal or InDel-in-tumor with SNV-in-normal at the same position. "),
    
    BcfFormatStruct("note"  , 1,         BCF_STRING,  "Additional note as comment for the given variant. ")
]

# This file is automatically generated by <script_name>. All changes to this file will be lost after recompilation!!!

FILTER_VEC = [
    # Example of FILTER_VEC contents, actual values need to be filled
    ('FILTER1', 'Description for filter 1'),
    ('FILTER2', 'Description for filter 2'),
    # Add more filters as necessary
]

FORMAT_VEC = [
    # Example of FORMAT_VEC contents, actual values need to be filled
    {'id': 'GT', 'type': 'string', 'description': 'Genotype', 'in_num_1': 1, 'out_num_2': 1, 'is_not_in_out_vcf': False, 'is_SSCS_required': False},
    {'id': 'AD', 'type': 'int', 'description': 'Allelic Depth', 'in_num_1': 1, 'out_num_2': 1, 'is_not_in_out_vcf': False, 'is_SSCS_required': True},
    # Add more formats as necessary
]

# This function is needed to get the proper header string for the 'Number' attribute in VCF format
def vcf_number_to_header_str(number):
    if number == 1:
        return '1'
    elif number == 'A':
        return 'A'
    elif number == 'G':
        return 'G'
    elif number == 'R':
        return 'R'
    return '.'  # Default case
def generate_bcf_formats():
    itnum = 0
    output = []

    # Comment for auto-generated file
    output.append("# This file is automatically generated by <script_name>. All changes to this file will be lost after recompilation!!!")
    
    # No need for C++ preprocessor directives like #ifndef, #define, #include, and namespaces in Python
    # In Python, we just skip them
    output.append("# FILTER_NUM = {0}".format(len(FILTER_VEC)))

    # Convert FILTER_ENUM to Python-style enum or list of keys
    output.append("FILTER_ENUM = [")
    for filter in FILTER_VEC:
        format_key = filter[0]
        output.append(f"    \"{format_key}\",")
    output.append("]")

    # Convert FILTER_IDS to Python-style list of strings
    output.append("FILTER_IDS = [")
    for filter in FILTER_VEC:
        filter_key = filter[0]
        output.append(f"    \"{filter_key}\",")
    output.append("]")

    # Convert FILTER_LINES to Python-style list of strings
    output.append("FILTER_LINES = [")
    for filter in FILTER_VEC:
        filter_key = filter[0]
        description = filter[1]
        output.append(f"    \"##FILTER=<ID={filter_key},Description=\\\"{description}\\\">\",")
    output.append("]")

    # Check for EXTRA_VCF_INFO (skip in Python if not defined)
    output.append("if OUTPUT_EXTRA_VCF_INFO:")
    output.append("    FILTER_DESCS = [")
    for filter in FILTER_VEC:
        filter_desc = filter[1]
        output.append(f"        \"{filter_desc}\",")
    output.append("    ]")

    # Format number equivalent in Python
    output.append("FORMAT_NUM = {0}".format(len(FORMAT_VEC)))

    # Convert FORMAT_ENUM to Python-style list of ids
    output.append("FORMAT_ENUM = [")
    for fmt in FORMAT_VEC:
        output.append(f"    \"{fmt['id']}\",")
    output.append("]")

    # Format string per record
    output.append("FORMAT_STRING_PER_REC = \"\"")
    itnum = 0
    for fmt in FORMAT_VEC:
        if fmt['is_not_in_out_vcf']:
            continue
        if itnum:
            output.append(":")
        output.append(fmt['id'])
        itnum += 1
    output.append("\"")

    # Format string per record without SSCS
    output.append("FORMAT_STRING_PER_REC_WITHOUT_SSCS = \"\"")
    itnum = 0
    for fmt in FORMAT_VEC:
        if fmt['is_not_in_out_vcf'] or fmt['is_SSCS_required']:
            continue
        if itnum:
            output.append(":")
        output.append(fmt['id'])
        itnum += 1
    output.append("\"")

    # Format IDs (list of ids in Python)
    output.append("FORMAT_IDS = [")
    for fmt in FORMAT_VEC:
        output.append(f"    \"{fmt['id']}\",")
    output.append("]")

    # Convert struct-like BcfFormat to Python class
    output.append("class BcfFormat:")
    output.append("    enable_tier2_consensus_format_tags = False")

    # Format entries
    for fmt in FORMAT_VEC:
        type_str = fmt['type']
        id_str = fmt['id']
        if fmt['in_num_1'] == 0 or fmt['in_num_1'] == 1:
            output.append(f"    {id_str} = {type_str}()")
        elif fmt['in_num_1'] > 1:
            output.append(f"    {id_str} = [{type_str}()] * {fmt['in_num_1']}")
        else:
            output.append(f"    {id_str} = []")

    output.append("")

    # Python equivalent of streamAppendBcfFormat
    output.append("def streamAppendBcfFormat(outstring, fmt):")
    itnum = 0
    for fmt in FORMAT_VEC:
        if fmt['is_not_in_out_vcf']:
            output.append(f"    # The FORMAT/TAG {fmt['id']} is skipped")
            itnum += 1
            continue
        addcheck = f"if fmt.enable_tier2_consensus_format_tags" if fmt['is_SSCS_required'] else "if True"
        output.append(f"    {addcheck}:")
        if itnum:
            output.append("        outstring += \":\"")
        if fmt['type'] == 'SEP':
            output.append(f"        outstring += FORMAT_IDS[{itnum}] + \"\"")
        else:
            output.append(f"        outstring += str(fmt.{fmt['id']})")
        output.append("")
        itnum += 1
    output.append("    return 0")

    # Python equivalent of resetBcfFormatD
    output.append("def resetBcfFormatD(fmt):")
    for fmt in FORMAT_VEC:
        if fmt['in_num_1'] == 'D':
            output.append(f"    fmt.{fmt['id']} = []")
    output.append("    return 0")

    # Python equivalent of streamFrontPushBcfFormatR
    output.append("def streamFrontPushBcfFormatR(dst, src):")
    for fmt in FORMAT_VEC:
        if fmt['in_num_1'] == 'R':
            output.append(f"    assert len(dst.{fmt['id']}) == 1")
            output.append(f"    assert len(src.{fmt['id']}) == 1")
            output.append(f"    {fmt['id']}_tmp = dst.{fmt['id']}[0]")
            output.append(f"    dst.{fmt['id']}[0] = src.{fmt['id']}[0]")
            output.append(f"    dst.{fmt['id']}.append({fmt['id']}_tmp)")
    output.append("    return 0")

    # Format lines for VCF headers
    output.append("FORMAT_LINES = [")
    for fmt in FORMAT_VEC:
        output.append(f"    \"##FORMAT=<ID={fmt['id']},Number={vcf_number_to_header_str(fmt['out_num_2'])},Type={fmt['type']},Description=\\\"{fmt['description']}\\\">\",")
    output.append("]")

    # If extra VCF format info is present, include additional fields
    output.append("if OUTPUT_EXTRA_VCF_FORMAT:")
    output.append("    FORMAT_NUMBERS = [")
    for fmt in FORMAT_VEC:
        output.append(f"        {fmt['out_num_2']},")
    output.append("    ]")

    output.append("    FORMAT_DATA_TYPES = [")
    for fmt in FORMAT_VEC:
        output.append(f"        \"{fmt['type']}\",")
    output.append("    ]")

    output.append("    FORMAT_DESCRIPTIONS = [")
    for fmt in FORMAT_VEC:
        output.append(f"        \"{fmt['description']}\",")
    output.append("    ]")

    output.append("")
    
    # Return joined output as a string
    return "\n".join(output)

# Output the generated file content
print(generate_bcf_formats())
print("Program run successfully.")
