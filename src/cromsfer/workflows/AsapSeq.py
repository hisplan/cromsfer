#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "AsapSeq.logHtoDemux": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-HtoDemuxKMeans/demux_kmeans.log",
    #   "AsapSeq.adataRaw": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-ToAnnData/ASAPseq_test_HTO_IGO_11671_3.h5ad",
    #   "AsapSeq.umiCountMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/features.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/matrix.mtx.gz"
    #   ],
    #   "AsapSeq.readCountMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/features.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/matrix.mtx.gz"
    #   ],
    #   "AsapSeq.logHtoDemux_Suppl1": null,
    #   "AsapSeq.reformattedR1": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-ReformatAsapSeqFastq/cacheCopy/ASAPseq_test_HTO_IGO_11671_3_R1.fastq.gz",
    #   "AsapSeq.adataFinal": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-UpdateAnnData/ASAPseq_test_HTO_IGO_11671_3.h5ad",
    #   "AsapSeq.countReport": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-CiteSeqCount/results/run_report.yaml",
    #   "AsapSeq.htoClassification_Suppl3": null,
    #   "AsapSeq.reformattedR2": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-ReformatAsapSeqFastq/cacheCopy/ASAPseq_test_HTO_IGO_11671_3_R2.fastq.gz",
    #   "AsapSeq.htoClassification_Suppl2": null,
    #   "AsapSeq.statsHtoDemux_Suppl1": null,
    #   "AsapSeq.fastQCR1Html": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-FastQCR1/cacheCopy/ASAPseq_test_HTO_IGO_11671_3_R1_fastqc.html",
    #   "AsapSeq.htoClassification_Suppl1": null,
    #   "AsapSeq.htoClassification": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-HtoDemuxKMeans/classification.tsv.gz",
    #   "AsapSeq.statsHtoDemux": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-HtoDemuxKMeans/stats.yml",
    #   "AsapSeq.fastQCR2Html": "s3://dp-lab-gwf-core/cromwell-execution/AsapSeq/dbc6304d-26bf-42a1-b3bb-4fa65ffaf7a6/call-Preprocess/Preprocess/ce493bee-ed3a-4a8c-8753-d0acfe03f553/call-FastQCR2/cacheCopy/ASAPseq_test_HTO_IGO_11671_3_R2_fastqc.html"
    # }

    items = list()

    items.append(
        (outputs["AsapSeq.countReport"], base_destination + "/counts/")
    )

    for file in outputs["AsapSeq.umiCountMatrix"]:
        items.append(
            (file, base_destination + "/counts/umis/")
        )

    for file in outputs["AsapSeq.readCountMatrix"]:
        items.append(
            (file, base_destination + "/counts/reads/")
        )

    items.append(
        (outputs["AsapSeq.fastQCR1Html"], base_destination + "/fastq/reformatted/")
    )
    items.append(
        (outputs["AsapSeq.fastQCR2Html"], base_destination + "/fastq/reformatted/")
    )

    items.append(
        (outputs["AsapSeq.reformattedR1"], base_destination + "/fastq/reformatted/")
    )
    items.append(
        (outputs["AsapSeq.reformattedR2"], base_destination + "/fastq/reformatted/")
    )

    items.append(
        (outputs["AsapSeq.adataRaw"], base_destination + "/")
    )
    items.append(
        (outputs["AsapSeq.adataFinal"], base_destination + "/")
    )

    items.append(
        (outputs["AsapSeq.htoClassification"], base_destination + "/")
    )

    return items
