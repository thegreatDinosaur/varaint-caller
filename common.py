# Import constants from commonDeclaration.py
from commonClasses import *
# Mapping ASSAY_TYPE to descriptive messages
ASSAY_TYPE_TO_MSG = [
    "Assay type of each molecule fragment will be automatically inferred from the data",  # ASSAY_TYPE_AUTO
    "Data is generated from a capture-based assay with selection by probe hybridization", # ASSAY_TYPE_CAPTURE
    "Data is generated from an amplicon-based assay with targeted amplification by PCR"   # ASSAY_TYPE_AMPLICON
]

# Mapping MOLECULE_TAG to descriptive messages
MOLECULE_TAG_TO_MSG = [
    "Molecule tag of each molecule fragment will be automatically inferred from the data",  # MOLECULE_TAG_AUTO
    "Molecule is not tagged",                                                              # MOLECULE_TAG_NONE
    "Molecule is tagged with a unique molecular identifier (UMI) on one strand as in Safe-SeqS",  # MOLECULE_TAG_BARCODING
    "Molecule is tagged with a duplex UMI"                                                 # MOLECULE_TAG_DUPLEX
]

# Mapping SEQUENCING_PLATFORM to descriptive messages
SEQUENCING_PLATFORM_TO_MSG = [
    "Unknown sequencing platform that will be automatically inferred from the data",  # SEQUENCING_PLATFORM_AUTO
    "Illumina sequencing platform (compatible with BGI and MGI)",                    # SEQUENCING_PLATFORM_ILLUMINA
    "IonTorrent sequencing platform by Life Technologies and ThermoFisher",          # SEQUENCING_PLATFORM_IONTORRENT
    "Other sequencing platform (for example, Nanopore)"                              # SEQUENCING_PLATFORM_OTHER
]

# Mapping SEQUENCING_PLATFORM to short names
SEQUENCING_PLATFORM_TO_NAME = [
    "AUTO",                   # SEQUENCING_PLATFORM_AUTO
    PLAT_ILLUMINA_LIKE,       # SEQUENCING_PLATFORM_ILLUMINA
    PLAT_ION_LIKE,            # SEQUENCING_PLATFORM_IONTORRENT
    "OtherSequencingPlatform" # SEQUENCING_PLATFORM_OTHER
]

# Mapping PAIR_END_MERGE to descriptive messages
PAIR_END_MERGE_TO_MSG = [
    "paired-end sequenced segments are merged",       # PAIR_END_MERGE_YES
    "paired-end sequenced segments are not merged"    # PAIR_END_MERGE_NO
]
