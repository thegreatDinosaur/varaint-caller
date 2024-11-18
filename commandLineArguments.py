import os
import argparse
import sys
import numpy as np
from collections import defaultdict

BQ_PHRED_ADDED_MISMA_IONTORRENT = 8
SYSERR_MINABQ_SNV_ILLUMINA = 200
SYSERR_MINABQ_INDEL_ILLUMINA = 100

def replace_underscore_with_hyphen(astring: str) -> str:
    return astring.replace('_', '-')

def stringvec_to_phrase(v: list) -> str:
    if not v:
        return ""
    if len(v) == 1:
        return v[0]
    return ", ".join(v[:-1]) + " and " + v[-1]

def stringvec_to_descstring(v: list) -> str:
    return "".join([f"{i} : {s}. " for i, s in enumerate(v)])

def check_file_exist(fname: str, ftype: str) -> None:
    if not os.path.exists(fname):
        print(f"The file {fname} of type ({ftype}) does not exist.")
        exit(-4)

class CommandLineArgs:
    def __init__(self, bam_input_fname, sequencing_platform, central_readlen=0):
        self.bam_input_fname = bam_input_fname
        self.sequencing_platform = sequencing_platform
        self.central_readlen = central_readlen
        self.inferred_maxMQ = 0
        self.fam_thres_highBQ_snv = 30
        self.fam_thres_highBQ_indel = 30
        self.bias_thres_PFBQ1 = 30
        self.bias_thres_PFBQ2 = 30
        self.bias_thres_highBQ = 13

    def self_update_by_platform(self):
        inferred_sequencing_platform = self.sequencing_platform
        if self.sequencing_platform == "SEQUENCING_PLATFORM_AUTO" or self.sequencing_platform == "SEQUENCING_PLATFORM_OTHER":
            with open(self.bam_input_fname, "rb") as sam_infile:
                countPE = 0
                countSE = 0
                qlens = [150]
                q20_n_fail_bases = 0
                q30_n_fail_bases = 0
                q30_n_pass_bases = 0
                for _ in range(5000):  
                    self.inferred_maxMQ = max(self.inferred_maxMQ, 30)
                    if countPE + countSE < 5000:
                        countPE += 1 if countPE % 2 == 0 else 0
                        countSE += 1 if countSE % 2 == 0 else 0
                    qlens.append(150)
                    q30_n_fail_bases += 10
                    q30_n_pass_bases += 140

                qlens.sort()
                if self.central_readlen == 0:
                    self.central_readlen = qlens[len(qlens)//2]

                isPE = countPE > 0
                is_2x_Q20toQ30_lessthan_Q30plus = 2 * (q30_n_fail_bases - q20_n_fail_bases) < q30_n_pass_bases
                is_4x_Q20toQ30_lessthan_Q30plus = 4 * (q30_n_fail_bases - q20_n_fail_bases) < q30_n_pass_bases
                isfixqlen = qlens[len(qlens)//2] * 100 > qlens[-1] * 95

                if isPE or is_4x_Q20toQ30_lessthan_Q30plus or (is_2x_Q20toQ30_lessthan_Q30plus and isfixqlen):
                    inferred_sequencing_platform = "SEQUENCING_PLATFORM_ILLUMINA"
                else:
                    inferred_sequencing_platform = "SEQUENCING_PLATFORM_IONTORRENT"

                print(f"Inferred_sequencing_platform={inferred_sequencing_platform}")
                print(f"IsPairedEnd={isPE}")
                print(f"is 2*BQ30<(BQ30-BQ20) passed = {is_2x_Q20toQ30_lessthan_Q30plus}")
                print(f"is 4*BQ30<(BQ30-BQ20) passed = {is_4x_Q20toQ30_lessthan_Q30plus}")
                print(f"isFixedReadQuerySeqLength = {isfixqlen}")

        if inferred_sequencing_platform == "SEQUENCING_PLATFORM_IONTORRENT" and self.sequencing_platform != "SEQUENCING_PLATFORM_OTHER":
            self.bq_phred_added_indel = 0
            self.bq_phred_added_misma = BQ_PHRED_ADDED_MISMA_IONTORRENT
            self.syserr_minABQ_pcr_snv = 0
            self.syserr_minABQ_pcr_indel = 0
            self.syserr_minABQ_cap_snv = 0
            self.syserr_minABQ_cap_indel = 0
            self.fam_thres_highBQ_snv = max(0, self.fam_thres_highBQ_snv - 30)
            self.fam_thres_highBQ_indel = max(0, self.fam_thres_highBQ_indel - 30)
            self.bias_thres_PFBQ1 = max(0, self.bias_thres_PFBQ1 - 30)
            self.bias_thres_PFBQ2 = max(0, self.bias_thres_PFBQ2 - 30)
            self.bias_thres_highBQ = max(0, self.bias_thres_highBQ - 13)

        if inferred_sequencing_platform == "SEQUENCING_PLATFORM_ILLUMINA" and self.sequencing_platform != "SEQUENCING_PLATFORM_OTHER":
            self.bq_phred_added_indel = 0
            self.bq_phred_added_misma = 0
            self.syserr_minABQ_pcr_snv = SYSERR_MINABQ_SNV_ILLUMINA
            self.syserr_minABQ_pcr_indel = SYSERR_MINABQ_INDEL_ILLUMINA
            self.syserr_minABQ_cap_snv = SYSERR_MINABQ_SNV_ILLUMINA
            self.syserr_minABQ_cap_indel = SYSERR_MINABQ_INDEL_ILLUMINA

        return inferred_sequencing_platform


VERSION = "1.0.0"  
VERSION_DETAIL = "Detailed version information here"  

class CommandLineArgs:
    def __init__(self):
        self.bam_input_fname = ""
        self.fasta_ref_fname = ""
        self.vcf_out_pass_fname = ""
    
    def init_from_args(self, args=None):
        if args is None:
            args = sys.argv[1:]

        parser = argparse.ArgumentParser(description=f"UVC version {VERSION_DETAIL}")

        parser.add_argument("-v", "--version", action="version", version=f"uvc-{VERSION}",
                            help="Show the version of this program.")

        parser.add_argument("inputBAM", metavar="inputBAM", type=str, 
                            help="The input coordinate-sorted and indexed BAM file that is supposed to contain raw reads. "
                                 "If set to 'OPT_ONLY_PRINT_VCF_HEADER', then only print the VCF header, that describes the output format and is not instantiated from the input files, and then exit with the exit code of zero. "
                                 "Important warnings about potential mis-use and mis-understanding are mentioned with the keyword CAVEAT in the VCF header.")
        
        parser.add_argument("-f", "--fasta", metavar="fasta_ref", type=str, 
                            help="The input reference FASTA file to which the inputBAM is aligned, where the special value NA means not available.")

        parser.add_argument("-o", "--output", metavar="vcf_out_pass", type=str, 
                            help="The output bgzipped VCF file. "
                                 "If this parameter is set to either the empty string ('') or dot ('.') and the --fam-consensus-out-fastq parameter is not set to either the empty string ('') or dot ('.'), "
                                 "then do not generate any VCF.")

        parsed_args = parser.parse_args(args)

        self.bam_input_fname = parsed_args.inputBAM
        self.fasta_ref_fname = parsed_args.fasta
        self.vcf_out_pass_fname = parsed_args.output

        

def main():
    parser = argparse.ArgumentParser(description="Command-line tool for genomic variant calling")

    # 01. parameters of the names of files, samples, regions, etc
    parser.add_argument(
        "-R", "--regions-file", 
        type=str, 
        help="Optional input BED region file which delimits the genomic regions to call variants from. "
             "If not provided, call variants from all sequenced genomic regions. This overrides the -t parameter. "
             "Ensure each region here is small enough to prevent memory exhaustion. Typically, each region covers one exon."
    )
    parser.add_argument(
        "--targets", 
        type=str, 
        help="Optional input region string (e.g., chr1:2-3 or chr1) to delimit the genomic region to call variants from. "
             "If not provided, variants are called from all sequenced genomic regions."
    )
    parser.add_argument(
        "-s", "--sample", 
        type=str, 
        help="Sample name (optional)."
    )

    parser.add_argument(
        "-t", "--threads", 
        type=int, 
        help="Number of CPU cores or threads to use."
    )
    parser.add_argument(
        "--outvar-flag", 
        type=int, 
        help="Output-variant flag in bits specifying which type of variants are in the VCF output."
    )
    parser.add_argument(
        "-q", "--vqual", 
        type=int, 
        help="Minimum variant quality for variants to be included in the output VCF."
    )

    parser.add_argument(
        "--assay-type", 
        type=int, 
        help="Assay type."
    )

    parser.add_argument(
        "--tumor-vcf", 
        type=str, 
        help="VCF file of the tumor sample to use with the normal BAM file."
    )

    parser.add_argument(
        "--fam-consensus-out-fastq", 
        type=str, 
        help="Filename prefix for the output FASTQ file generated by the tier-1 consensus of fragments."
    )

    parser.add_argument(
        "--bed-out-fname", 
        type=str, 
        help="BED file to which genomic-region information will be written."
    )

    parser.add_argument(
        "--bed-in-fname", 
        type=str, 
        help="BED file from which genomic-region information is read. This overrides the --regions-file parameter."
    )

    parser.add_argument(
        "--bed-in-avg-sequencing-DP", 
        type=int, 
        help="Average sequencing depth in the BED input file. If -1, inferred from the input BAM file."
    )

    parser.add_argument(
        "--bed-in-avg-sequencing-DP-n-from-t", 
        type=int, 
        help="If set to 1, the number of reads covered by each BED region is taken from the corresponding tumor BAM."
    )

    parser.add_argument(
        "--is-tumor-format-retrieved", 
        type=int, choices=[0, 1], 
        help="Indicates if the format from the tumor VCF should be retrieved in the tumor-normal comparison."
    )
    parser.add_argument(
        "--kept-aln-min-aln-len", 
        type=int, 
        help="Minimum alignment length below which the alignment is filtered out."
    )
    parser.add_argument(
        "--kept-aln-min-mapqual", 
        type=int, 
        help="Minimum mapping quality below which the alignment is filtered out."
    )
    parser.add_argument(
        "--kept-aln-min-isize", 
        type=int, 
        help="Minimum insert size below which the alignment is filtered out (not applicable to zero insert size)."
    )
    parser.add_argument(
        "--kept-aln-max-isize", 
        type=int, 
        help="Maximum insert size above which the alignment is filtered out."
    )
    parser.add_argument(
        "--kept-aln-is-zero-isize-discarded", 
        type=int, choices=[0, 1], 
        help="Indicates if an alignment with zero insert size should be filtered out."
    )

    parser.add_argument(
        "--min-altdp-thres", 
        type=int, 
        help="Minimum allele depth below which allele records are not in the output VCF."
    )
    parser.add_argument(
        "--vdp1", 
        type=int, 
        help="Total depth of highBQ segments for variant alleles."
    )
    parser.add_argument(
        "--vad1", 
        type=int, 
        help="Allele depth of highBQ segments for variant alleles."
    )
    parser.add_argument(
        "--vfa1", 
        type=float, 
        help="Allele fraction of highBQ segments for variant alleles."
    )

    parser.add_argument(
        "--vdp2", 
        type=int, 
        help="Total depth of fragments for variant alleles."
    )
    parser.add_argument(
        "--vad2", 
        type=int, 
        help="Allele depth of fragments for variant alleles."
    )
    parser.add_argument(
        "--vfa2", 
        type=float, 
        help="Allele fraction of fragments for variant alleles."
    )

    parser.add_argument(
        "--min-r-ad", 
        type=int, 
        help="Minimum reference allele depth of fragments to be included in the VCF."
    )
    parser.add_argument(
        "--min-a-ad", 
        type=int, 
        help="Minimum variant allele depth of fragments to be included in the VCF."
    )    
    parser.add_argument(
        "--should-add-note", 
        action="store_true", 
        help="Flag to generate more detailed information in the VCF result file for debugging."
    )
    parser.add_argument(
        "--always-log", 
        action="store_true", 
        help="Flag to generate detailed log results to stderr."
    )
    parser.add_argument(
        "--molecule-tag", 
        type=str, 
        help="Molecule tag, such as a UMI (unique molecular identifier) used for read grouping."
    )
    parser.add_argument(
        "--sequencing-platform", 
        type=int, 
        help="Sequencing platform used for sequencing (e.g., Illumina, Ion Torrent)."
    )
    parser.add_argument(
        "--pair-end-merge", 
        type=int, 
        help="Mode for merging R1 and R2 in a paired-end read."
    )
    parser.add_argument(
        "--disable-duplex", 
        action="store_true", 
        help="Flag indicating if duplex reads should not be merged into double-strand consensus sequences."
    )

    
 

