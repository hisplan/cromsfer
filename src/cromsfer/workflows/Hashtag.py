#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "Hashtag.umiCountMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-CiteSeqCount/cacheCopy/glob-5b2373ebac80816456a7726e786fc4d4/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-CiteSeqCount/cacheCopy/glob-5b2373ebac80816456a7726e786fc4d4/features.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-CiteSeqCount/cacheCopy/glob-5b2373ebac80816456a7726e786fc4d4/matrix.mtx.gz"
    #   ],
    #   "Hashtag.countReport": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-CiteSeqCount/cacheCopy/results/run_report.yaml",
    #   "Hashtag.fastQCR1Html": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-FastQCR1/cacheCopy/1973_HD1915_7xNK_FB_HTO_R1_fastqc.html",
    #   "Hashtag.fastQCR2Html": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-FastQCR2/cacheCopy/1973_HD1915_7xNK_FB_HTO_R2_fastqc.html",
    #   "Hashtag.combinedCountMatrix": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-HashedCountMatrix/final-matrix.tsv.gz",
    #   "Hashtag.adataRaw": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-ToAnnData/1973_HD1915_7xNK_FB_HTO.h5ad",
    #   "Hashtag.adataFinal": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-UpdateAnnData/1973_HD1915_7xNK_FB_HTO.h5ad",
    #   "Hashtag.statsHtoDemux_Suppl1": null,
    #   "Hashtag.combinedClass": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-HashedCountMatrix/final-classification.tsv.gz",
    #   "Hashtag.htoClassification_Suppl1": null,
    #   "Hashtag.logHtoDemux_Suppl1": null,
    #   "Hashtag.htoClassification": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-HtoDemuxKMeans/cacheCopy/classification.tsv.gz",
    #   "Hashtag.combinedStats": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-HashedCountMatrix/stats.yml",
    #   "Hashtag.statsHtoDemux": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-HtoDemuxKMeans/cacheCopy/stats.yml",
    #   "Hashtag.readCountMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-CiteSeqCount/cacheCopy/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-CiteSeqCount/cacheCopy/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/features.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-Preprocess/Preprocess/744288fb-47e7-49ef-83e1-d79443b5b9d3/call-CiteSeqCount/cacheCopy/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/matrix.mtx.gz"
    #   ],
    #   "Hashtag.htoClassification_Suppl3": null,
    #   "Hashtag.combinedLog": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-HashedCountMatrix/combine.log",
    #   "Hashtag.htoClassification_Suppl2": null,
    #   "Hashtag.logHtoDemux": "s3://dp-lab-gwf-core/cromwell-execution/Hashtag/c3a941bf-62ed-469e-8ee6-d7448cdee457/call-HtoDemuxKMeans/cacheCopy/demux_kmeans.log"
    # }

    items = list()

    items.append(
        (outputs["Hashtag.countReport"], base_destination + "/counts/")
    )

    for file in outputs["Hashtag.umiCountMatrix"]:
        items.append(
            (file, base_destination + "/counts/umis/")
        )

    for file in outputs["Hashtag.readCountMatrix"]:
        items.append(
            (file, base_destination + "/counts/reads/")
        )

    items.append(
        (outputs["Hashtag.fastQCR1Html"], base_destination + "/fastqc/")
    )
    items.append(
        (outputs["Hashtag.fastQCR2Html"], base_destination + "/fastqc/")
    )

    items.append(
        (outputs["Hashtag.adataRaw"], base_destination + "/")
    )
    items.append(
        (outputs["Hashtag.adataFinal"], base_destination + "/")
    )

    # optional output
    if outputs["Hashtag.combinedCountMatrix"]:
        items.append(
            (outputs["Hashtag.combinedCountMatrix"], base_destination + "/")
        )

    # optional output
    if outputs["Hashtag.combinedClass"]:
        items.append(
            (outputs["Hashtag.combinedClass"], base_destination + "/")
        )

    return items
