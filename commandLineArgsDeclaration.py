import math
import sys

# Constants
NOT_PROVIDED = "."
NUM_FQLIKE_CON_OUT_FILES = 3
FASTQ_LIKE_SUFFIXES = ["R1.fastq.gz", "R2.fastq.gz", "SE.fastq.gz"]
DEBUG_NOTE_FLAG_BITMASK_BAQ_OFFSETARR = 0x1

# Define the CommandLineArgs class
class CommandLineArgs:
    def __init__(self):
        # *** 00. frequently used parameters
        self.bam_input_fname = NOT_PROVIDED
        self.fasta_ref_fname = NOT_PROVIDED
        self.vcf_out_pass_fname = "-"
        self.bed_region_fname = NOT_PROVIDED
        self.tier1_target_region = NOT_PROVIDED
        self.sample_name = "-"
        self.max_cpu_num = 8
        self.mem_per_thread = (1024 * 3 // 2)  # MegaBytes
        
        # Flag and other boolean params
        self.outvar_flag = 0xF1  # OUTVAR_SOMATIC + OUTVAR_ANY + OUTVAR_MGVCF + OUTVAR_BASE_NN + OUTVAR_ADDITIONAL_INDEL_CANDIDATE
        self.should_output_all = False
        self.should_output_all_germline = False
        self.vqual = 15.0
        
        # Assay Type and threshold values
        self.assay_type = "ASSAY_TYPE_AUTO"
        self.fam_thres_highBQ_snv = 25
        self.fam_thres_highBQ_indel = 13
        self.fam_thres_dup1add = 2
        self.fam_thres_dup1perc = 80
        self.fam_thres_dup2add = 3
        self.fam_thres_dup2perc = 70
        self.fam_thres_qseqlen = 75
        self.fam_consensus_out_fastq = ""
        self.fam_consensus_out_fastq_thres_dup1add = 1
        
        # *** 01. parameters of the names of files, samples, regions, etc.
        self.vcf_tumor_fname = NOT_PROVIDED
        self.bed_out_fname = NOT_PROVIDED
        self.bed_in_fname = NOT_PROVIDED
        self.bed_in_avg_sequencing_DP = -1
        self.bed_in_avg_sequencing_DP_n_from_t = 0x0
        
        # *** 02. parameters that control input, output, and logs (driven by computational requirements and resources)
        self.is_tumor_format_retrieved = True
        self.kept_aln_min_aln_len = 0
        self.kept_aln_min_mapqual = 0
        self.kept_aln_min_isize = 0
        self.kept_aln_max_isize = sys.maxsize
        self.kept_aln_is_zero_isize_discarded = False
        self.min_altdp_thres = 2
        self.vdp1 = 1000
        self.vad1 = 4
        self.vfa1 = 0.002
        self.vdp2 = 10000
        self.vad2 = 8
        self.vfa2 = 0.0002
        self.min_r_ad = 0
        self.min_a_ad = 0
        self.should_add_note = False
        self.always_log = False
        
        # *** 03. parameters that are driven by the properties of the assay
        self.molecule_tag = "MOLECULE_TAG_AUTO"
        self.sequencing_platform = "SEQUENCING_PLATFORM_AUTO"
        self.inferred_sequencing_platform = self.sequencing_platform
        self.inferred_maxMQ = 0
        self.pair_end_merge = "PAIR_END_MERGE_YES"
        self.disable_duplex = False
        self.primerlen = 0
        self.primerlen2 = 23
        self.primer_flag = 0x0
        self.central_readlen = 0
        self.bq_phred_added_misma = 0
        self.bq_phred_added_indel = 0
        self.powlaw_exponent = 3.0
        self.powlaw_anyvar_base = 60 + 25 + 5
        self.powlaw_amplicon_allele_fraction_coef = 5.0 / 8.0
        
        # *** 04. parameters for dedupping reads
        self.dedup_center_mult = 5
        self.dedup_amplicon_end2end_ratio = 1.5
        self.dedup_amplicon_border_to_insert_cov_weak_avgDP_ratio = 5
        self.dedup_amplicon_border_to_insert_cov_strong_avgDP_ratio = 20
        self.dedup_amplicon_border_to_insert_cov_weak_totDP_ratio = 0.05
        self.dedup_amplicon_border_to_insert_cov_strong_totDP_ratio = 0.20
        self.dedup_amplicon_border_weak_minDP = 100
        self.dedup_amplicon_border_strong_minDP = 400
        self.dedup_flag = 0x0
        
        # *** 05. parameters related to bias thresholds
        self.bias_thres_highBQ = 20
        self.bias_thres_highBAQ = 20
        self.bias_thres_aLPxT_add = 5
        self.bias_thres_aLPxT_perc = 160
        self.bias_thres_PFXM1T_add = 130
        self.bias_thres_PFXM2T_add = 20
        self.bias_thres_PFGO1T_add = 125
        self.bias_thres_PFGO2T_add = 15
        
        # *** 06. parameters related to the priors of bias
        self.bias_prior_DPadd_perc = 50
        self.bias_priorfreq_pos = 40
        self.bias_priorfreq_indel_in_read_div = 20
        self.bias_priorfreq_indel_in_var_div2 = 15
        self.bias_priorfreq_indel_in_str_div2 = 10
        self.bias_priorfreq_var_in_str_div2 = 5
        
        # *** 07. parameters related to read families
        self.fam_thres_emperr_all_flat_snv = 4
        self.fam_thres_emperr_con_perc_snv = 67
        self.fam_thres_emperr_all_flat_indel = 4
        self.fam_thres_emperr_con_perc_indel = 67
        self.fam_min_n_copies = 800
        self.fam_min_n_copies_DPxAD = 20 * 1000
        self.fam_min_overseq_perc = 200
        self.fam_bias_overseq_perc = 150
        self.fam_tier3DP_bias_overseq_perc = 350
        self.fam_indel_nonUMI_phred_dec_per_fold_overseq = 9
        
        # *** 08. parameters related to systematic errors
        self.syserr_BQ_prior = 30
        self.syserr_BQ_sbratio_q_add = 5
        self.syserr_BQ_sbratio_q_max = 40
        self.syserr_BQ_xmratio_q_add = 5
        self.syserr_BQ_xmratio_q_max = 40
        self.syserr_BQ_bmratio_q_add = 5
        self.syserr_BQ_bmratio_q_max = 40
        self.syserr_BQ_strand_favor_mul = 3
        self.syserr_MQ_min = 0
        self.syserr_MQ_max = 60
        self.syserr_MQ_NMR_expfrac = 0.03
        self.syserr_MQ_NMR_altfrac_coef = 2.0
        self.syserr_MQ_NMR_nonaltfrac_coef = 2.0
        self.syserr_MQ_NMR_pl_exponent = 3.0
        self.syserr_MQ_nonref_base = 40
        
        # *** 09. parameters related to germline vars
        self.germ_hetero_FA = 0.47
        self.germ_phred_hetero_snp = 31
        self.germ_phred_hetero_indel = 41 - 1
        self.germ_phred_homalt_snp = 31 + 2
        self.germ_phred_homalt_indel = 41 - 1 + 2
        self.germ_phred_het3al_snp = 54 + 5
        self.germ_phred_het3al_indel = 41 - 1 + 9
        
        # *** 10. parameters related to tumor-normal-pairs
        self.tn_q_inc_max = 9
        self.tn_q_inc_max_sscs_CG_AT = 0
        self.tn_q_inc_max_sscs_other = 5
        self.tn_syserr_norm_devqual = 15.0
        self.tn_is_paired_end = False
        self.tn_q_cutoff_min_ratio = 0.1
        self.tn_q_cutoff_max_ratio = 1.0
        
        # *** 11. parameters related to statistical tests
        self.test_n_convs_mq_weakmax = 10
        self.test_n_convs_mq_strongmax = 10
        self.test_n_convs_baq_weakmax = 8
        self.test_n_convs_baq_strongmax = 8
        self.test_frac_baq_leq = 0.9
        self.test_frac_baq_geq = 0.8
        self.test_frac_mq_leq = 0.9
        self.test_frac_mq_geq = 0.8
        
        # *** 12. additional flags
        self.test_bq_add_note = False
        self.test_mq_add_note = False
        self.test_baq_add_note = False
        
        # Additional parameters to handle specific details of data processing
        self.keep_track_of_last_processed_pos = 0
        self.keep_track_of_last_processed_refpos = 0
        self.max_num_rounds = 100
        self.applied_filter_flag = 0
        
        # *** 13. parameter for logging
        self.debug_bitmask = 0x0
        
        # *** 14. internal debug flags
        self.debug_is_output_all = False
        self.debug_is_output_no_qual = False
        self.debug_is_output_debug = False
        self.debug_is_output_all_dbg_info = False
        self.debug_is_output_family_dbg_info = False
        self.debug_is_output_family_count = False
        self.debug_is_output_family_count_dbg_info = False
        self.debug_is_output_quality = False
        self.debug_is_output_seq = False
        self.debug_is_output_gene_stats = False
        
        # *** 15. error correction parameters
        self.correct_alignment_flag = 0x0
        self.max_error_num = 15
        self.max_cov_err_allowed = 0.03

# Function to parse command line arguments into the CommandLineArgs class
def parse_cmdline_args(argv):
    args = CommandLineArgs()
    
    # This is a simple example of how you might begin parsing command-line arguments.
    # This would need to be expanded based on your specific needs.
    for i in range(1, len(argv)):
        if argv[i] == "--bam-input":
            args.bam_input_fname = argv[i + 1]
        elif argv[i] == "--fasta-ref":
            args.fasta_ref_fname = argv[i + 1]
        elif argv[i] == "--vcf-output":
            args.vcf_out_pass_fname = argv[i + 1]
        # Add more argument parsing as necessary
        
    return args

# Example of using the class
if __name__ == "__main__":
    args = parse_cmdline_args(sys.argv)
    print(f"BAM input file: {args.bam_input_fname}")
    print(f"FASTA reference file: {args.fasta_ref_fname}")
    print(f"VCF output file: {args.vcf_out_pass_fname}")
