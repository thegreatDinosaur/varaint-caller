from enum import Enum
import commonClasses

# Enums to represent assay type, molecule tag, sequencing platform, and pair end merge options
class AssayType(Enum):
    AUTO = 0
    CAPTURE = 1
    AMPLICON = 2

class MoleculeTag(Enum):
    AUTO = 0
    NONE = 1
    BARCODING = 2
    DUPLEX = 3

class SequencingPlatform(Enum):
    AUTO = 0
    ILLUMINA = 1
    IONTORRENT = 2
    OTHER = 3

class PairEndMerge(Enum):
    YES = 0
    NO = 1

# Function to get the message for each assay type
def get_assay_type_msg(assay_type: AssayType) -> str:
    return commonClasses.ASSAY_TYPE_TO_MSG[assay_type.value]

# Function to get the message for each molecule tag
def get_molecule_tag_msg(molecule_tag: MoleculeTag) -> str:
    return commonClasses.MOLECULE_TAG_TO_MSG[molecule_tag.value]

# Function to get the message for each sequencing platform
def get_sequencing_platform_msg(sequencing_platform: SequencingPlatform) -> str:
    return commonClasses.SEQUENCING_PLATFORM_TO_MSG[sequencing_platform.value]

# Function to get the name for each sequencing platform
def get_sequencing_platform_name(sequencing_platform: SequencingPlatform) -> str:
    return commonClasses.SEQUENCING_PLATFORM_TO_NAME[sequencing_platform.value]

# Function to get the message for pair end merge
def get_pair_end_merge_msg(pair_end_merge: PairEndMerge) -> str:
    return commonClasses.PAIR_END_MERGE_TO_MSG[pair_end_merge.value]
