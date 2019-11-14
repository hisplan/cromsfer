#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # outSeqcFiles
    # [
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_alignment_summary.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cell_filters.png",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_0_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_1_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_2_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_3_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_4_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_5_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_6_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_7_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_8_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_cluster_9_mast_input.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_de_gene_list.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_dense.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1.h5",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_mini_summary.html",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_mini_summary.json",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_mini_summary.pdf",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_pca.png",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_phenograph.png",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_sparse_counts_barcodes.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_sparse_counts_genes.csv",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_sparse_molecule_counts.mtx",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_sparse_read_counts.mtx",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-SEQC/glob-c45bdb4787237de1991565574c79fe53/TKO12_week_1_summary.tar.gz"
    # ]

    # outStarFiles
    # [
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/Genome",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SA",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SAindex",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/annotations.gtf",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrLength.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrName.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrNameLength.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrStart.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonGeTrInfo.tab",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonInfo.tab",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/geneInfo.tab",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/genomeParameters.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbInfo.txt",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.fromGTF.out.tab",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.out.tab",
    #   "s3://dp-lab-batch/cromwell-execution/SeqcCustomGenes/ca139a63-35ad-4b08-9cf8-09feb1af1b29/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/transcriptInfo.tab"
    # ]

    items = list()

    for key in outputs.keys():

        if key == "SeqcCustomGenes.outSeqcFiles":
            # fixme: not implemented
            pass
        elif key == "SeqcCustomGenes.outStarFiles":
            for file in outputs[key]:
                items.append(
                    (file, base_destination + "/genome/")
                )

    return items
