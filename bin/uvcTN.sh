#!/usr/bin/env bash

scriptdir="$(dirname "$(which "$0")")"
if [ $# -lt 5 ]; then
    echo "Usage: $0 <REF> <tumorBam> <normalBam> <outputName> <tumorSampleName>[,<normalSampleName>][/<nprocs>[,<nprocs2>]/<parallel|qsub>] [<allParams>] [--tumor-params <tumorParams>] [--normal-params <normalParams>]"
    echo "  The output bgzipped vcf file is "
    echo "    <outputName> (with <outputName>.byproduct/<tumorSampleName>_T_uvc1.vcf.gz as intermediate tumor vcf) if <normalSampleName> is provided or "
    echo "    <outputName>/<tumorSampleName>_N_uvc1.vcf.gz (with <outputName>/<tumorSampleName>_T_uvc1.vcf.gz as intermediate tumor vcf) if normalSampleName is not provided. "
    echo "  <nprocs> is the number of processes corresponding to the number of chromosomes that are run concurrently in parallel, "
    echo "    where 0 (zero, which is the default value) means no chromosome-level parallelization. "
    echo "  <nprocs2> is the number of threads used by bcftools. "
    echo "  <parallel|qsub> means the string parallel or qsub. "
    echo "    The string parallel requires GNU parallel to be installed and the string qsub requires the variable UVC_QSUB_CMD to be set. "
    echo "    For example, UVC_QSUB_CMD can be \"qsub -V -S /bin/sh\". "
    echo "    Please note that the qsub option is deprecated because of two reasons: "
    echo "      1. The number of qsub commands is equal to the number of reference fasta sequences. "
    echo "      1. Afterwards, the user has to manually merge the VCF results generated from their respective reference fasta sequences. "
    echo "    More commands result in more output files and more overhead. " 
    echo "    Therefore, please do not use the qsub option especially if the reference fasta file contains a lot of sequences. "
    echo "  <allParams> is the set of command-line parameters (i.e. arguments) to ${scriptdir}/uvc1 for both tumor and normal samples. "
    echo "    --tumor-params is optional and is followed by the parameters to ${scriptdir}/uvc1 for only the  tumor-sample. "
    echo "    --normal-params is optional and is followed by the parameters to ${scriptdir}/uvc1 for only the normal-sample. "
    echo "  For help on the usage of \"${scriptdir}/uvc1\", please enter \"${scriptdir}/uvc1\" -h "
    exit 1
fi

tstate=1
nstate=1
tparams=()
nparams=()
for p in "${@:6}"; do
    cstate=0
    if [[ "${p}" = "--tumor-params" ]]; then
        tstate=1
        nstate=0
        cstate=1
    elif [[ "${p}" = "--normal-params" ]]; then
        tstate=0
        nstate=1
        cstate=1
    fi
    if [ $cstate -eq 0 ]; then
        if [ $tstate -eq 1 ]; then
            tparams+=($p)
        fi
        if [ $nstate -eq 1 ]; then
            nparams+=($p)
        fi
    fi
done

echo "cmdLineArgParser.infoMessage.T: the command-line parameters are ( ${tparams[@]} ) for generating the tumor vcf"
echo "cmdLineArgParser.infoMessage.N: the command-line parameters are ( ${nparams[@]} ) for generating the normal vcf"

set -evx

if [ -z "${UVC_BIN_EXE_FULL_NAME}" ]; then
    UVC_BIN_EXE_FULL_NAME="${scriptdir}/uvc1"
else
    echo "WARNING: using UVC_BIN_EXE_FULL_NAME=${UVC_BIN_EXE_FULL_NAME} from environment variable."
    echo "Please enter the shell command (unset UVC_BIN_EXE_FULL_NAME) before running uvcTN.sh if the default uvc binary exe full path should be used."
fi

ref="$1"
tbam="$2"
nbam="$3"
samplename=$(echo "$5/0/parallel" | awk -F"/" '{print $1}')
nprocsa=$(echo "$5/0/parallel" | awk -F"/" '{print $2}')
nprocs=$(echo "${nprocsa}" | awk -F"," '{print $1}')
nprocs2=$(echo "${nprocsa},4" | awk -F"," '{print $2}')
paratool=$(echo "$5/0/parallel" | awk -F"/" '{print $3}')

if [ $(echo "${samplename}" | awk -F "," '{print NF}') -eq 2 ]; then
    tsample=$(echo "${samplename}" | awk -F "," '{print $1}')
    nsample=$(echo "${samplename}" | awk -F "," '{print $2}')
    outdir="${4}.byproduct"
    nvcfgz="${4}"
else
    tsample="${samplename}_T"
    nsample="${samplename}_N"
    outdir="$4"
    nvcfgz="${outdir}/${nsample}_uvc1.vcf.gz"
fi
nlog="${outdir}/${nsample}_uvc1.stderr"
tvcfgz="${outdir}/${tsample}_uvc1.vcf.gz"
tlog="${outdir}/${tsample}_uvc1.stderr"
tbed="${outdir}/${tsample}_uvc1.bed"
mkdir -p "${outdir}"

export PATH="${scriptdir}:${PATH}" # remove this line in the rare case that an important executable is shadowed by this command

if [ "${nprocs}" -gt 0 ]; then
    tnames=$(cat "${ref}.fai" | awk '{print $1}')
    if [ "${paratool}" = "parallel" ]; then
        mkdir -p "${outdir}/parallel-results/"
        for tname in ${tnames}; do
            echo "${0}" "${ref}" "${tbam}" "${nbam}" "${outdir}/parallel-results/${tname}.uvc1.vcf.gz" "${tsample},${nsample}" --targets "${tname}" "${@:6}" 
        done > "${outdir}/run_parallel.sh"
        cat "${outdir}/run_parallel.sh" | parallel -j "${nprocs}"
        bcftools concat -n -Oz -o "${nvcfgz}" "${outdir}/parallel-results/"*".uvc1.vcf.gz"
        bcftools index -ft --threads "${nprocs2}" "${nvcfgz}"
    elif [ "${paratool}" = "qsub" ]; then
        echo "The use of the qsub command that is automatically generated by this script is deprecated! Please consider using either "
        echo "  1) the intrinsic multithreading capability in UVC with the -t option to the UVC binary executable or " 
        echo "  2) GNU parallel for multiprocessing. "
        if [ -z "${UVC_QSUB_CMD}" ]; then
            echo "The variable UVC_QSUB_CMD must be set and exported in order to use qsub! "
            exit -2
        fi
        for tname in ${tnames}; do
            echo echo "${0}" "${ref}" "${tbam}" "${nbam}" "${outdir}/${tname}" "${samplename}" --targets "${tname}" "${@:6}" "|" "${UVC_QSUB_CMD}" -o "${outdir}" -e "${outdir}" -v JOB_NAME="${tname}.job"
        done > "${outdir}/run_qsub.sh"
        sh "${outdir}/run_qsub.sh"
    else
        echo "The multiprocessing tool ${paratool} is neither parallel nor qsub. "
        exit -1
    fi
else
    date
    "${UVC_BIN_EXE_FULL_NAME}" -f "${ref}" -s "${tsample}" "${tbam}" -o "${tvcfgz}" --tn-is-paired 1 --bed-out-fname "${tbed}" "${tparams[@]}" 2> "${tlog}"
    date 
    bcftools index -ft --threads "${nprocs2}" "${tvcfgz}" # or use tabix, requires htslib 1.6 or plus

    date
    "${UVC_BIN_EXE_FULL_NAME}" -f "${ref}" -s "${nsample}" "${nbam}" -o "${nvcfgz}" --tn-is-paired 1 --bed-in-fname  "${tbed}" "${nparams[@]}" --tumor-vcf "${tvcfgz}" 2> "${nlog}"
    date
    bcftools index -ft --threads "${nprocs2}" "${nvcfgz}" # or use tabix, requires htslib 1.6 or plus
fi

date
exit 0

